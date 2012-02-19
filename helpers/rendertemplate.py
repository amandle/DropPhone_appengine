import os
from google.appengine.ext.webapp import template

def rendertemplate(template_file_name, params={}):
  path = os.path.join(os.path.dirname(__file__),'../templates/',template_file_name)
  return template.render(path,params)
