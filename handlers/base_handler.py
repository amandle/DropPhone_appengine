import os
from google.appengine.ext import webapp
from helpers.rendertemplate import rendertemplate

class BaseHandler(webapp.RequestHandler):
  def render(self,template,params):
    common_params = {
      'APP_VERSION':os.environ.get('CURRENT_VERSION_ID','no-version-set')
    }
    final_params = dict(  common_params.items() + params.items())
    self.response.out.write(rendertemplate(template,final_params))

