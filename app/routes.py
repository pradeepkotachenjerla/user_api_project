import re
from flask import request, jsonify
from app import app, db
from app.models import User, Profile

def is_valid_name(name):
    return isinstance(name, str) and name.strip() != ''

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return isinstance(email, str) and re.match(pattern, email)

def is_valid_age(age):
    try:
        age = int(age)
        return 1 <= age <= 120
    except (TypeError, ValueError):
        return False

# User CRUD
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    age = data.get('age')
    if not is_valid_name(name):
        return jsonify({'error': 'Name must be a non-empty string'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if age is not None and not is_valid_age(age):
        return jsonify({'error': 'Age must be between 1 and 120'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    user = User(name=name, email=email, age=age)
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
    name = data.get('name', user.name)
    email = data.get('email', user.email)
    age = data.get('age', user.age)
    if not is_valid_name(name):
        return jsonify({'error': 'Name must be a non-empty string'}), 400
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    if age is not None and not is_valid_age(age):
        return jsonify({'error': 'Age must be between 1 and 120'}), 400
    if email != user.email and User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    user.name = name
    user.email = email
    user.age = age
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# Profile CRUD
@app.route('/profiles', methods=['POST'])
def create_profile():
    data = request.get_json()
    if not data or not data.get('user_id'):
        return jsonify({'error': 'user_id is required'}), 400
    if not User.query.get(data['user_id']):
        return jsonify({'error': 'User does not exist'}), 404
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
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
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
