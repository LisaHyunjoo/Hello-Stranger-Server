import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

posts = Blueprint('posts', 'posts')

@posts.route('/', methods=['POST'])
@login_required
def create_posts():
    payload = request.get_json()
    print(payload)
    new_post = models.Post.create(user=current_user.id, title=payload['title'], content=payload['content'], comment=payload['comment'])
    print(new_post)

    post_dict = model_to_dict(new_post)

    post_dict['user'].pop('password')

    return jsonify(
        data=post_dict,
        message = "created a new post",
        status=201
    ), 201

@posts.route('/', methods=["GET"])
def posts_index():
    result = models.Post.select()
    print(result)

    current_user_post_dicts = [model_to_dict(post) for post in current_user.posts]

    for post_dict in current_user_post_dicts:
        post_dict['user'].pop('password')

    return jsonify({
        'data':current_user_post_dicts,
        'message':"success",
        "status":200
    }),200

@posts.route('/<id>', methods=["GET"])
def get_one_post(id):
    post = models.Post.get_by_id(id)
    del post['user']['password']

    return jsonify(
        data = model_to_dict(post),
        message = "success",
        status = 200
    ),200
    
