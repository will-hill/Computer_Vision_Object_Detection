import os
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button
from bokeh.plotting import figure, show, output_file
import base64
from os.path import join, dirname
import logging

# ### CODE FROM https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/EtuMtJI39qQ
_upload_js = """
function read_file(filename) {
    // alert('read_file');
    var reader = new FileReader();
    reader.onload = load_handler;
    reader.onerror = error_handler;
    // readAsDataURL represents the file's data as a base64 encoded string
    reader.readAsDataURL(filename);
}

function load_handler(event) {
    // alert('load_handler');
    var b64string = event.target.result;
    source.data = {'contents' : [b64string], 'name':[input.files[0].name]};
    source.change.emit()
}

function error_handler(evt) {
    // alert('error_handler');
    if(evt.target.error.name == "NotReadableError") {
        alert("Can't read file!");
    }
}

var input = document.createElement('input');
input.setAttribute('type', 'file');
input.onchange = function(){
    if (window.FileReader) {
        read_file(input.files[0]);
    } else {
        alert('FileReader is not supported in this browser');
    }
}
input.click();
"""

save_path = dirname(__file__)

def file_callback(attr, old, new):
    name = 'tmp.png'
    raw_contents = source.data['contents'][0]
    # name = source.data['name'][0]
    # remove the prefix that JS adds
    prefix, b64_contents = raw_contents.split(",", 1)
    file_contents = base64.b64decode(b64_contents)
    fname = join(save_path, name)
    with open(fname, "wb") as f:
        f.write(file_contents)
    logging.info("Success: file uploaded " + fname)
    name = fname
    update(fname)


source = ColumnDataSource({'contents': [], 'name': []})
source.on_change('data', file_callback)

button = Button(label="Upload File", button_type="success")
button.callback = CustomJS(args=dict(source=source), code=_upload_js)

# Set up plot
p = figure(x_range=(0, 1), y_range=(0, 1))

def update(file_path):
    print('attempting: ' + file_path + '\n\n')

    image = 'tmp.png'
    image_ints = ColumnDataSource(dict(url=[image]))
    p = figure(plot_width=500, plot_height=500, title="")
    p.image_url(url='url', x=0.05, y=0.85, h=0.7, w=0.9, source=image_ints)
    # p.image_url(url=['tmp.png'], x=0, y=0, w=1, h=1, anchor="bottom_left")
    # p.image_url(url=['tmp.png'], x=0, y=0, w=1, h=1, anchor="bottom_left")
    # p.image_url(url=[file_path], x=0, y=0, w=1, h=1, anchor="bottom_left")
    # p.image(image=[file_path], x=0, y=0, dw=10, dh=10, palette="Spectral11")
    # p.image(image=[file_path],  x=0, y=0, w=1, h=1, anchor="bottom_left")
    # curdoc().add_root(row(button, p))
    # curdoc().title = "Upload"
    # show(p)
    # curdoc()


# update(name)
# show(p)
#curdoc().add_root(page_logo)
curdoc().add_root(row(button, p))
curdoc().title = "Upload"
