import os
import warnings
import nexmo
from flask import Flask, json, render_template, url_for, request, session
import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

myapp = Flask(__name__)

@myapp.route('/predict', methods=['POST'])
def predict():
    # model = pickle.load(open("../model/spam_model.pkl", "rb"))
    # tfidf_model = pickle.load(open("../model/tfidf_model.pkl", "rb"))
    if request.method == "POST":
        bool_is_json = request.is_json
        if not bool_is_json:
            return json.jsonify("{\"result\": \"invalid JSON format\"}"), 400
        else:
            id = request.json.get("id", None)
            number = request.json.get("number", None)
            message = request.json.get("message_body", None)
            print("request components : ")
            print("id : ", id)           
            print("number : ", number)
            print("message: ", message)
            spam = False
            # str = {"result" : "This be a valid req niqqa", "id": "" + id + ""}
            result = {"result" : "This be a valid req niqqa", "id": "" + id + "", "spam" : "" + str(spam) + ""}
            return json.dumps(result)
            # return json.jsonify("{\"result\" : \"This be a valid req niqqa\", \"id\": \"" + id + "\"}"), 200
            # return json.jsonify("{'result' : 'This be a valid req niqqa', 'id': '" + id + "'}"), 200
    else:
            return json.jsonify("{\"result\": \"API only responds to POST request\"}"), 400

if __name__ == '__main__':
    myapp.run(port=5000, debug=True)