import numpy as np
import os
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure
import base64
from os.path import join, basename
import logging

# ### CODE FROM https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/EtuMtJI39qQ

def new_upload_button(save_path, callback, name="tmp.las", label="Upload file."):
    def file_callback(attr, old, new):
        raw_contents = source.data['contents'][0]
        # remove the prefix that JS adds
        prefix, b64_contents = raw_contents.split(",", 1)
        file_contents = base64.b64decode(b64_contents)
        fname = join(save_path, name)
        with open(fname, "wb") as f:
            f.write(file_contents)
        logging.info("Success: file uploaded " + fname)
        callback(fname)

    source = ColumnDataSource({'contents': [], 'name': []})
    source.on_change('data', file_callback)

    button = Button(label=label, button_type="success")
    button.callback = CustomJS(args=dict(source=source), code=_upload_js)
    return button, source


_upload_js = """
function read_file(filename) {
    var reader = new FileReader();
    reader.onload = load_handler;
    reader.onerror = error_handler;
    // readAsDataURL represents the file's data as a base64 encoded string
    reader.readAsDataURL(filename);
}

function load_handler(event) {
    var b64string = event.target.result;
    source.data = {'contents' : [b64string], 'name':[input.files[0].name]};
    source.change.emit()
}

function error_handler(evt) {
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

save_path = os.getcwd()
name = 'temp.esi'


def file_callback(attr, old, new):
    raw_contents = source.data['contents'][0]
    # remove the prefix that JS adds
    prefix, b64_contents = raw_contents.split(",", 1)
    file_contents = base64.b64decode(b64_contents)
    fname = join(save_path, name)
    with open(fname, "wb") as f:
        f.write(file_contents)
    logging.info("Success: file uploaded " + fname)
    update(fname)


source = ColumnDataSource({'contents': [], 'name': []})
source.on_change('data', file_callback)

button = Button(label="Upload File", button_type="success")
button.callback = CustomJS(args=dict(source=source), code=_upload_js)
# Set up plot
p = figure(x_range=(0, 1), y_range=(0, 1))


def update(fname):
    p.image_url(url=[fname], x=0, y=1, w=1, h=1)


update("temp.esi")
curdoc().title = "Image Loader"
curdoc().add_root(row(button, p))
curdoc().title = "Upload"
