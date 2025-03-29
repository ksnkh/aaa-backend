import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
import logging
import io
from image_server_client import ImageServerClient
from requests.exceptions import Timeout


app = Flask(__name__)
img_client = ImageServerClient()
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')


@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {
        'plate_number': res,
    }


@app.route('/id/<img_id>', methods=['GET'])
def number_from_id(img_id):
    try:
        img_io = img_client.fetch_image_data(img_id)
    except Timeout:
        return {'error': "Could not fetch the image"}, 500
    except Exception as e:
        return {'error': str(e)}, 400

    try:
        res = plate_reader.read_text(img_io)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': "Could not parse the image"}, 500
    return {
        'plate_number': res,
    }


@app.route('/readplates', methods=['POST'])
def sum_numbers():
    data = request.json
    try:
        images = {id: img_client.fetch_image_data(id) for id in data['ids']}
    except Timeout:
        return {'error': "Could not fetch the image"}, 500
    except Exception as e:
        return {'error': str(e)}, 400

    try:
        res = {id: plate_reader.read_text(img_io) for (id, img_io) in images.items()}
    except InvalidImage:
        logging.error('invalid image')
        return {'error': "Could not parse the image"}, 500
    return res

if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
