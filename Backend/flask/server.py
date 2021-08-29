import os
from flask import Flask, request, jsonify, make_response
import random
from jina import Document
from werkzeug.serving import WSGIRequestHandler
import base64
from cockroach import Cockroach
import io
from PIL import Image

from werkzeug.utils import send_file
from werkzeug.wrappers import response
app = Flask(__name__)

@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
    return "Hello world!"


def fetchImageJina(imageName):
  '''
  Use this function to search for Images similar to that image. It takes in the name of the image. The name as which it is saved as in the disk.
  Then this function will send the best match Jina could find
  '''
  import cv2
  import requests
  x = cv2.imread(imageName)
  doc = Document(content = x)
  doc.convert_image_blob_to_uri(width=100, height=100)
  headers = {
        'Content-Type': 'application/json',
    }
  data = '{"top_k":1,"mode":"search","data":["' + doc.uri + '"]}'

  response = requests.post(
          'http://172.28.90.71:45678/search', headers=headers, data=data)
  res = response.json()
  return res["data"]['docs'][0]['matches'][0]['text']

def fetchTextJina(searchText):
  '''
  Use this function to search for images in Jina. This function takes in the text for which you would like to search the images for.
  Try Calling this function as fetchImageJina("BasketBall") and this function will return the best image match. It will save the best match image in the disk
  and return the name of the image which it is saved as
  '''
  
  import requests
  import cv2
  text = searchText
  headers = {
        'Content-Type': 'application/json',
    }
  data = '{"parameters":{"top_k": 7},"data":["' + text + '"]}'
  response = requests.post(
          'http://172.28.90.71:45678/search', headers=headers, data=data)
  res = response.json()

  return_array = []
  for i, v in enumerate(res['data']['docs'][0]['matches']):
    doc = Document(v)
    img_name = "{name}.jpg".format(name = i)
    return_array.append(img_name)
    cv2.imwrite(img_name, cv2.cvtColor(doc.blob, cv2.COLOR_RGB2BGR))
  return return_array




@app.route('/image', methods = ['POST' , 'GET'])
def hola():
    image = request.files['picture']
    print(image.filename)
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))
    return_text = fetchImageJina(image_name)
    return jsonify({'ans':return_text})


@app.route('/search', methods=['POST'])
def search():
  response = request.get_json(force= True, silent= True)
  # print(response)
  # print(response['search'])
  return_image = fetchTextJina(response['search'])
  return_list =[]
  for i in return_image:

    with open(i, 'rb') as image_file:
      encoded_string = base64.b64encode(image_file.read())
    return_list.append(str(encoded_string))
  return jsonify({'image':return_list})

if __name__ == '__main__':
  WSGIRequestHandler.protocol_version = "HTTP/1.1"
  app.run(host='0.0.0.0', port=12345) # This line is required to run Flask on repl.it 




