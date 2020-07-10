# **It took me 3 hours to solve this assignment.**
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
            'No, it isn\'t. Multiple formats like JSON or XML may be used by appending something like ?format=json as '
            'a query option to the url or by using the HTTP Accept header. There is no real standard for doing that.',
        'Are all operations on this REST APIs idempotent? Explain why! (1 Point)':
            'REST APIs should make all operations idempotent where the HTTP verb is not POST.'
            'POST requests cannot be idempotent since they insert new data and return the ID of'
            'the newly created datapoint, which by definition needs to be unique',
        'Why could it be problematic to work with complete URLs (with protocol, hostname and path) as links? Name and '
        'explain two reasons (2 Points)': [
            'If you decide to use a new server (with another hostname), then all of your URLs would be invalid and '
            'you would need to change them. The same goes for changing to another protocol.',
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

    return json.dumps(result), 200


@V1.route('/images', methods=['GET'])
def get_images():
    # get options from request
    # in case of invalid parameters return 400
    try:
        limit = int(request.args.get('limit', default='100'))
        offset = int(request.args.get('offset', default='0'))
    except ValueError:
        return json.dumps({'message': 'Invalid limit or offset passed!'}), 400
    if limit < 1 or limit > 500 or offset < 0:
        return json.dumps({'message': 'Invalid limit or offset passed!'}), 400

    count = Image.select().count()  # pylint: disable=no-value-for-parameter
    image_dict = {'images': [], 'count': count}

    # iterate over all images with given offset and limit
    # wrap them into json and add them to the list
    for image in Image.select().limit(limit).offset(offset):
        image_json = get_image_json_object(image)
        image_dict['images'].append(image_json)
    return json.dumps(image_dict), 200


@V1.route('/images/<int:imageid>', methods=['GET'])
def get_image_by_id(imageid):
    # select image with matching id and return 404 if no such image found
    image = Image.select().where(Image.id == imageid)
    if image.count() == 0:
        return json.dumps({'message': 'No image with matching ID found!'}), 404
    # wrap image object into JSON and return it
    image_json = {'image': get_image_json_object(image[0])}
    return json.dumps(image_json), 200


@V1.route('/images/<int:imageid>/bitmap', methods=['GET'])
def get_bitmap_by_id(imageid):
    # select image with matching id and return 404 if no such image found
    image = Image.select().where(Image.id == imageid)
    if image.count() == 0:
        return json.dumps({'message': 'No image with matching ID found!'}), 404
    # forward request to image source using proxy
    return proxy.stream(request, 'GET', BASE_URL_DATASET + image[0].src)


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

    # This line starts a new transaction and automatically commits it at the end of the with-clause
    # It is needed because database operations can fail. Then, the transaction would have to be aborted.
    # The with-clause also takes care of this and issues a rollback.
    with database_holder.database.transaction():
        # Empty databases
        Image.delete().execute()  # pylint: disable=no-value-for-parameter
        Caption.delete().execute()  # pylint: disable=no-value-for-parameter

        tree = html.fromstring(answer.text)

        # for every picture (corresponds to tr)
        for pictureTree in tree.xpath('/html/body/table/tr'):
            # get source and category
            src = pictureTree.xpath('td/img/@src')[0]
            category = re.match(r'(\w+)\/', src).group(1)

            # save Image in DB, nothing magical here
            imageDb = Image(src=src, category=category)
            imageDb.save()

            #  get all captions and save them
            for captionTree in pictureTree.xpath('td//td'):
                caption_text = captionTree.text[1:]
                Caption(text=caption_text, image=imageDb).save()

    return json.dumps({'status': 'finished'}), 200
