from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profiles = db.relationship('Profile', backref='user', lazy=True)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(255))
    social_links = db.Column(db.Text)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], age=data.get('age'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'age': u.age} for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/profiles', methods=['POST'])
def create_profile():
    data = request.get_json()
    profile = Profile(user_id=data['user_id'], bio=data.get('bio'), profile_picture_url=data.get('profile_picture_url'), social_links=data.get('social_links'))
    db.session.add(profile)
    db.session.commit()
    return jsonify({'id': profile.id}), 201

@app.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([{'id': p.id, 'user_id': p.user_id, 'bio': p.bio, 'profile_picture_url': p.profile_picture_url, 'social_links': p.social_links} for p in profiles])

@app.route('/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    return jsonify({'id': profile.id, 'user_id': profile.user_id, 'bio': profile.bio, 'profile_picture_url': profile.profile_picture_url, 'social_links': profile.social_links})

@app.route('/profiles/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    data = request.get_json()
    profile.bio = data.get('bio', profile.bio)
    profile.profile_picture_url = data.get('profile_picture_url', profile.profile_picture_url)
    profile.social_links = data.get('social_links', profile.social_links)
    db.session.commit()
    return jsonify({'message': 'Profile updated'})

@app.route('/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'Profile deleted'})

if __name__ == '__main__':
    app.run(debug=True)
