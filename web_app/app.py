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
    if request.method == "POST":
        bool_is_json = request.is_json
        if not bool_is_json:
            jsonlist = []
            jsondict = {"error": "ERROR_INVALIDJSONFORMAT"}
            jsonlist.append(jsondict)
            mainjsondict = {"result": jsonlist}
            result = mainjsondict
            print("JSON error encountered")
            return json.dumps(result), 200
        else:
            model = pickle.load(open("../model/spam_model.pkl", "rb"))
            tfidf_model = pickle.load(open("../model/tfidf_model.pkl", "rb"))
            print("valid json")
            entries = request.json.get("entries", None)
            # print(entries)
            print("printing json entries")

            jsonlist = []
            jsonerror = False
            spam = False
            for jo in entries:
                jsondict = {}
                print("id = ", jo['id'])
                id = jo['id']
                #check if id is string
                if not isinstance(id, str):
                    jsonerror = True
                    break
                print("message_body = ", jo['message_body'])
                message = jo['message_body']
                #check if message is string
                if not isinstance(message, str):
                    jsonerror = True
                    break
                #process this message and predict spam or not, for now we will put dummy True and False alternatively
                
                message = [message]
                dataset = {'message': message}
                data = pd.DataFrame(dataset)
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
                
                jsondict['id'] = id
                jsondict['spam'] = str(my_prediction[0])
                # spam = not spam
                jsonlist.append(jsondict)
            
            if  jsonerror:
                print("JSON error encountered")
                jsonlist = []
                jsondict = {"error": "ERROR_INVALIDJSONFORMAT"}
                jsonlist.append(jsondict)
                mainjsondict = {"result": jsonlist}
                result = mainjsondict
                return json.dumps(result), 200

            print("printing jsonlist")
            print(jsonlist)
            mainjsondict = {"result": None}
            mainjsondict['result'] = jsonlist
            result = mainjsondict 
            return json.dumps(result)     
    else:
            result = {"result" : "API only responds o POST request"}, 400
            # return json.jsonify("{\"result\": \"API only responds to POST request\"}"), 400
            return json.dumps(result)

if __name__ == '__main__':
    myapp.run(host="0.0.0.0", port=5000, debug=True)
