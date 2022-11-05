import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

posts = Blueprint('posts', 'posts')

@posts.route('/', methods=['POST'])
def create_posts():
    payload = request.get_json()
    print(payload)
    new_post = models.Post.create(title=payload ['title'], content=payload['content'])
    print(new_post)

    post_dict = model_to_dict(new_post)

    return jsonify(
        data=post_dict,
        message = "created a new post",
        status=201
    ), 201

@posts.route('/', methods=["GET"])
def posts_index():
    result = models.Post.select()
    print('result of dog select query')
    print(result)

    post_dicts = [model_to_dict(post) for post in result]

    return jsonify({
        'data':post_dicts,
        'message':f"Successfully found {post_dicts}",
        "status":200
    }),200
    
