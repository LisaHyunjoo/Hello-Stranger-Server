import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

comments = Blueprint('comments', 'comments')

@comments.route("/<int:post_id>/comment", methods=['POST'])
@login_required
def create_a_comment(post_id):
    payload = request.get_json()
    print(payload)
    new_comment = models.Comment.create(user=current_user.id, 
    content=payload['content'], post=post_id )
    comment_dict = model_to_dict(new_comment)

    del comment_dict['user']['password']
    del comment_dict['post']['user']['password']


    return jsonify(
        data=comment_dict,
        message='created a new comment',
        status=201
    ),201

@comments.route("/<int:post_id>/comment", methods=['GET'])
def get_comments(post_id):
    comments = models.Comment.select().join(models.Post).where(models.Post.id == post_id)
    # print([model_to_dict(comment) for comment in comments])
    comment_dict = [model_to_dict(comment) for comment in comments]

    return jsonify({
        'data':comment_dict,
        'message':"success",
        'stats':200
    }), 200

@comments.route('/<int:post_id>/comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(post_id, comment_id):
    query = models.Comment.delete().where(models.Post.id == post_id and models.Comment.id == comment_id)
    query.execute()
    return jsonify(
        data = {},
        message="comment is deleted",
        status=200
    ), 200

@comments.route('/<int:post_id>/comment/<int:comment_id>', methods=['PUT'])
def update_a_comment(post_id, comment_id):
    payload = request.get_json()
    query = models.Comment.update(**payload).where(models.Post.id == post_id and models.Comment.id == comment_id)
    query.execute()
    return jsonify(
        data = model_to_dict(models.Comment.get_by_id(comment_id)),
        status=200,
        message='post is updated'
    ), 200
    

