from jinja2 import Template
from glob import glob
import os, os.path
from creds import imgdir

with open('gallery.jinja', 'r') as f:
    template = Template(f.read())

imglist = [os.path.basename(f) for f in glob(os.path.join(imgdir, '*.gif'))]
with open(os.path.join(imgdir, 'index.html'),'w') as f:
    f.write(template.render(imglist=imglist))

