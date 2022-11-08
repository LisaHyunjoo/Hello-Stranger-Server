import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user

comments = Blueprint('comments', 'comments')

@comments.route("/<id>", methods=['POST'])
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


# @comments.route("<id>", methods=['GET'])
# def get_comments():
    # comments = models.Comments.select()
    # print(comments)

    

