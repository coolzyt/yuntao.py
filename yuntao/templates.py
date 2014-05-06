#coding=utf8

from mako.template import Template
from mako.lookup import TemplateLookup
import os;
lookup = TemplateLookup(directories=[os.path.abspath('./')],
                         module_directory=os.path.abspath('./tmp/template_modules'),
                         output_encoding='utf-8',
                          input_encoding='utf-8',
                          encoding_errors='replace')

def render(templatepath,**kwargs):
    mytemplate = lookup.get_template(templatepath)
    return mytemplate.render(**kwargs)

def rendertext(text,**kwargs):
    return Template(text).render(**kwargs)