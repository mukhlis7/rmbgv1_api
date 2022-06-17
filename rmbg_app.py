#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,request, render_template,redirect,jsonify

from rembg import remove
import transfer
import requests

app = Flask(__name__)



app_passwd = 'mysecretMg7Mukhlis7HelloFromThisWorld!'

app.config['SECRET_KEY'] = app_passwd


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/upload_image2proc', methods=['POST'])
def image2proc():

    if request.method == 'POST':
        if 'file1' not in request.files:
            print("there is no file1 in request")
            resp = jsonify({'message' : 'there is no file1 in request'})
            return resp


        file = request.files['file1']
        filename = request.form.get('filename')
        print("File name:    " + str(filename))

        # if user does not select file, browser also
        # submit an empty part without filename
        if filename == '':
            print("filename empty")
            resp = jsonify({'message' : 'No selected file'})
            return resp
        if file and allowed_file(filename):
            print("ALLOWED_EXTENSIONS")
            output = remove(request.files['file1'].read())
            img_url = "https://transfer.sh/" + filename
            response = requests.put(img_url, data=output)
            up_file_link = response.content.decode("utf-8")
            resp = jsonify({'message' : 'Successfully Uploaded & Converted!', 'up_file_link' : up_file_link})
            return resp

        return "none executed!"
    return "method not allowed!"
    #return render_template('form.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)