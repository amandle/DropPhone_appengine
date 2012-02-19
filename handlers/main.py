import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
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
    logging.info('username ' + username)
    score = float(self.request.get('score'))
    s = ScoreEntry(
      score=float(score),
      username=username,
    )
    s.put()
    rank = 1
    scores = ScoreEntry.gql('order by score desc').fetch(1000)
    for scoreobj in scores:
      logging.info('conparing ' + str(scoreobj.score) + ' and ' + str(score))
      if scoreobj.score <= score:
        break
      else:
        rank += 1

    logging.info('Rank ' + str(rank))
    response = {
      'rank': rank
    }
    self.response.out.write(json.dumps(response))




def main():
  application = webapp.WSGIApplication(
    [('/', MainHandler),
     ('/leaderboard', LeaderBoardHandler),
     ('/app/newscore', ScoreHandler),
    ],
                                                           debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
