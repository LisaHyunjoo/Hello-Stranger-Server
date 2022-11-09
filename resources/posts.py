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
    new_post = models.Post.create(user=current_user.id, title=payload['title'], content=payload['content'])
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
    # del post['user']['password']

    return jsonify(
        data = model_to_dict(post),
        message = "success",
        status = 200
    ),200
    
    
@posts.route('/<id>', methods=['DELETE'])
def delete_post(id):
    query = models.Post.delete().where(models.Post.id == id)
    # print(model_to_dict(query))
    query.execute()
    return jsonify(
        data = {},
        message="post is deleted",
        status=200
    ), 200

@posts.route('/<id>', methods=['PUT'])
def update_post(id):
    payload = request.get_json()
    query = models.Post.update(**payload).where(models.Post.id == id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Post.get_by_id(id)),
        status=200,
        message='post is updated'
    ), 200