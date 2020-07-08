# Remove for testing with pylint ;)
# pylint: disable=fixme

# **It took me ? hours to solve this assignment.**
# Solved by (Matrikelnummern): 801005, 801123


import json
import re

from lxml import html

import requests
from flask import Blueprint, request

from flask_common.util import proxy

from app import database_holder

from app.models import Image, Caption

BASE = Blueprint('', __name__, url_prefix='')
V1 = Blueprint('v1', __name__, url_prefix='/v1')

BASE_URL_DATASET = 'https://image-annotations.marschke.me/NAACL/'


@V1.route('/health', methods=['GET'])
@BASE.route('/health', methods=['GET'])  # This route exists for the health check of the docker container
def check_health():
    return json.dumps({
        "status": "up",
        "message": "operational",
    }), 200


def get_image_json_object(image):
    caption_list = []

    for caption in image.captions:
        caption_list.append({
            'text': caption.text
        })
    return {
        'id': image.id,
        'category': image.category,
        'captions': caption_list,
    }


@V1.route('/tasks', methods=['GET'])
def get_tasks():
    return json.dumps({
        'taskList': [
            'Answer questions stated in get_answers() (5 Points)',
            'Build API defined in docs/swagger.yml (precise as possible) (23 Points)',
        ]
    })


# 2 Points code style:
#   Linter (each "real" error -0.5)
#   Readability (up to -2 if very "obfuscated")
#
# Bonus points for really nice solutions and approaches, which aren't covered by our solution / in our opinion nicer
# than in our solution

@V1.route('/answers', methods=['GET'])
def get_answers():
    result = {
        'Is a REST API bound to a single exchange format like JSON? How can multiple formats be used? (1 Point)':
            '',
        'Are all operations on this REST APIs idempotent? Explain why! (1 Point)':
            '',
        'Why could it be problematic to work with complete URLs (with protocol, hostname and path) as links? Name and '
        'explain two reasons (2 Points)': [
            '',
        ],
        'Hand in requirements (1 Point)': [
            'ZIP the complete source code directly from the root directory (so no useless subdirs in ZIP please)',
            'Make an own solution, show us that this is your solution by adding comments where they are needed to '
            'understand your source code',
            'Do not change any file names if not really needed (and then please document).',
            'Do not alter return definitions from functions get_tasks and get_answers.',
            'Write your answers in German or English, in code please write all English.',
            'Please write down your matriculation number at top of this file.',
            'Please add a comment at top of this file how much time you needed for this assignment (please be honest).',
        ]
    }

    for key in result:
        if key != 'Hand in requirements (1 Point)':
            result[key] = '[Solution hidden] Hey, what are you searching? A solution? Tzz. ;)'

    return json.dumps(result), 200


# TODO implement missing routes
# You can request images from the database by executing something like
# for image in Image.select().limit(limit).offset(offset):
#     do something with the image
#
# To access captions, you need to access image.captions for a list of all caption object (more precisely a generator)
#
# For counting all images in DB you can use this command: Image.select().count()
# If using pylint please add # pylint: disable=no-value-for-parameter to the end of the line.
#
# You can access GET arguments by request.args.get('key', 'default') where request is a global object defined by Flask
#
# For the bitmap route please proxy the image from the original source to your client. For this you can use this helper
# method: `from flask_common.util import proxy`

@V1.route('/images/fetch', methods=['POST'])
def update_image_storage():
    """This operation should clear DB if run multiple times on the same DB

    8 Points: 3 for xpath (1 each), 1 for correct resource GET, 2 for correct DB handling,
              1 for correct regex, 1 for Transaction explanation
    -0.5 for small mistakes (return value...)

    :return: json if successful or not
    """

    answer = requests.get(BASE_URL_DATASET)
    # Error handling
    answer.raise_for_status()

    # TODO Please explain what this line is doing. Why is it needed? In which case? (directly here as comment)
    with database_holder.database.transaction():
        # Empty databases
        Image.delete().execute()  # pylint: disable=no-value-for-parameter
        Caption.delete().execute()  # pylint: disable=no-value-for-parameter

        tree = html.fromstring(answer.text)

        for pictureTree in tree.xpath('/html/body/table/tr'):
            src = pictureTree.xpath('td/img/@src')[0]
            category = re.match(r'(\w+)\/', src).group(1)

            # save Image in DB, nothing magical here
            imageDb = Image(src=src, category=category)
            imageDb.save()

            for captionTree in pictureTree.xpath('td//td'):
                caption_text = captionTree.text[1:]
                Caption(text=caption_text, image=imageDb).save()

    return json.dumps({'status': 'finished'}), 200
