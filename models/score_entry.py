from google.appengine.ext import db

class ScoreEntry(db.Expando):
  username = db.StringProperty()
  score = db.FloatProperty()
  created = db.DateTimeProperty(auto_now_add=True)



