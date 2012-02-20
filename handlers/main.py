import logging
import random
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import hashlib
from handlers import config
from handlers.base_handler import BaseHandler
from models.score_entry import ScoreEntry
import simplejson as json

class MainHandler(BaseHandler):
  def get(self):
    top_scores = ScoreEntry.gql('order by score desc').fetch(10)
    self.render('home.html',{
      'top_scores':top_scores,

    })

class LeaderBoardHandler(BaseHandler):
  def get(self):
    top_scores = ScoreEntry.gql('order by score desc').fetch(50)
    self.render('leaderboard.html',{
      'top_scores':top_scores,
    })

class ScoreHandler(BaseHandler):
  def post(self):
    username = self.request.get('username')
    string_score = self.request.get('score')
    score = float(string_score)
    hash = self.request.get('hash')

    # verify the hash
    md5 = hashlib.md5()
#    sha.update(username)
    md5.update(string_score)
    md5.update(config.SHARED_SECRET)
    calcedhash = md5.hexdigest()
    if calcedhash != hash:
      logging.info('THE HASHES DO NOT MATCH ' + calcedhash + ' and ' + hash)
#      fake response
      response = {
        'rank': random.randint(1,9999)
      }
      self.response.out.write(json.dumps(response))
      return
    else:
      logging.info('they match!')


    s = ScoreEntry(
      score=score,
      username=username,
    )
    s.put()
    rank = 1
    scores = ScoreEntry.gql('order by score desc').fetch(1000)
    for scoreobj in scores:
      if scoreobj.score <= score:
        break
      else:
        rank += 1

    logging.info('Rank ' + str(rank))
    response = {
      'rank': rank
    }
    self.response.out.write(json.dumps(response))


class AboutHandler(BaseHandler):
  def get(self):
    self.render('about.html',{})

def main():
  application = webapp.WSGIApplication(
    [('/', MainHandler),
     ('/leaderboard', LeaderBoardHandler),
     ('/about', AboutHandler),
     ('/app/newscore', ScoreHandler),
    ],
                                                           debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
