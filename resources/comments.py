import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

comments = Blueprint('comments', 'comments')

@comments.route("/<id>/comment", methods=['POST'])
@login_required
def create_a_comment(id):
    payload = request.get_json()
    new_comment = models.Comment.create(user=current_user.id, 
    content=payload['content'], post=id )
    comment_dict = model_to_dict(new_comment)

    del comment_dict['user']['password']
    del comment_dict['post']['user']['password']


    return jsonify(
        data=comment_dict,
        message='created a new comment',
        status=201
    ),201

@comments.route("/<id>/comment", methods=['GET'])
def get_comments(id):
    comments = models.Comment.select().join(models.Post).where(models.Post.id == id)
    # print([model_to_dict(comment) for comment in comments])
    comment_dict = [model_to_dict(comment) for comment in comments]

    return jsonify({
        'data':comment_dict,
        'message':"success",
        'stats':200
    }), 200


    

