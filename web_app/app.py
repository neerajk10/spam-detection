import os
import warnings
import nexmo
from flask import Flask, json, render_template, url_for, request, session
import pickle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
# import lightgbm 

myapp = Flask(__name__)

@myapp.route('/predict', methods=['POST'])
def predict():
    model = pickle.load(open("../model/spam_model.pkl", "rb"))
    tfidf_model = pickle.load(open("../model/tfidf_model.pkl", "rb"))

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

            message = [message]
            dataset = {'message': message}
            data = pd.DataFrame(dataset)
            # data = pd.DataFrame({'message': message});
            data["message"] = data["message"].str.replace(
                r'^.+@[^\.].*\.[a-z]{2,}$', 'emailaddress')
            data["message"] = data["message"].str.replace(
                r'^http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$', 'webaddress')
            data["message"] = data["message"].str.replace(r'£|\$', 'money-symbol')
            data["message"] = data["message"].str.replace(
                r'^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$', 'phone-number')
            data["message"] = data["message"].str.replace(r'\d+(\.\d+)?', 'number')
            data["message"] = data["message"].str.replace(r'[^\w\d\s]', ' ')
            data["message"] = data["message"].str.replace(r'\s+', ' ')
            data["message"] = data["message"].str.replace(r'^\s+|\s*?$', ' ')
            data["message"] = data["message"].str.lower()

            stop_words = set(stopwords.words('english'))
            data["message"] = data["message"].apply(lambda x: ' '.join(
                term for term in x.split() if term not in stop_words))
            ss = nltk.SnowballStemmer("english")
            data["message"] = data["message"].apply(lambda x: ' '.join(ss.stem(term)
                                                                    for term in x.split()))

            # tfidf_model = TfidfVectorizer()
            tfidf_vec = tfidf_model.transform(data["message"])
            tfidf_data = pd.DataFrame(tfidf_vec.toarray())
            my_prediction = model.predict(tfidf_data)


            spam = my_prediction
            print("prediction: ")
            for pred in spam:
                print(pred)

            result = {"result" : "This is a valid req", "id": "" + id + "", "spam" : "" + str(spam) + ""}
            return json.dumps(result)
    else:
            result = {"result" : "API only responds o POST request"}, 400
            # return json.jsonify("{\"result\": \"API only responds to POST request\"}"), 400
            return json.dumps(result)

if __name__ == '__main__':
    myapp.run(port=5000, debug=True)
