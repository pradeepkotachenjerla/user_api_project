from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    profiles = db.relationship('Profile', backref='user', lazy=True)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(255))
    social_links = db.Column(db.Text)
