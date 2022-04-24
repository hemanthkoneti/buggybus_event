from buggybus import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(64))

    def __init__(self,username, password):
        self.username = username
        self.password = password

    def check_password(self,password):
        return self.password==password
    

db.create_all()
admin=User('Admin','ujpasswd123hskjahuashu')
user1=User('Hemanth','ujpasswd123hskjahuashu')
user2=User('Amit','ujpasswd123hskjahuashu')
db.session.add(admin)
db.session.add(user1)
db.session.add(user2)
db.session.commit()


