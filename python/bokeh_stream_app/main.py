import numpy as np
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

# import pandas

# pandas.read_csv(join(dirname(__file__), 'data', 'things.csv'))

save_path = dirname(__file__) + '/static/'

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


def update(file_path):
    print('attempting: ' + file_path + '\n\n')
    x = np.linspace(0, 4 * np.pi, 5)
    y = 13 * np.sin(12 * x + 4) + 2
    source.data = dict(x=x, y=y)
    img_path = 'bokeh_stream_app/static/tmp.png'
    p.image_url(url=[img_path], x=x_range[0], y=y_range[1], w=x_range[1] - x_range[0], h=y_range[1] - y_range[0])



# update(name)
# show(p)
#curdoc().add_root(page_logo)
# Set up plot
#p = figure(x_range=(0, 1), y_range=(0, 1))
x_range = (-20,-10) # could be anything - e.g.(0,1)
y_range = (20,30)
p = figure(x_range=x_range, y_range=y_range)
img_path = 'bokeh_stream_app/static/tmp.png'
p.image_url(url=[img_path],x=x_range[0],y=y_range[1],w=x_range[1]-x_range[0],h=y_range[1]-y_range[0])

doc = curdoc()

doc.add_root(row(button, p))
doc.title = "Upload"
