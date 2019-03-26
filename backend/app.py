from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

def load_ols_model():
    with open('models/pickle_model', 'rb') as pmodel:  
        pickle_model = pickle.load(pmodel)
        return pickle_model

ols_model = load_ols_model()

featureList = ['Java', 'Pages enabled', 'Issues enabled', 'Scala', 'PHP',
       'Python', 'Default branch', 'Size', 'Contributors Count',
       'Forks Count', 'Open Issues Count', 'Watchers Count', 'Emacs Lisp',
       'BSD-2-Clause', 'JavaScript', 'Wiki enabled', 'MIT',
       'Pull requests enabled', 'Fork', 'HTML', 'Other', 'CSS', 'Go',
       'Shell', 'Objective-C']

@app.route('/api/stars/predict', methods=['GET', 'POST'])
def ols_predict():
    body = pd.read_json(request.data, typ='series', dtype=int)
    testx = pd.read_csv('testdata.csv')
    testx = testx[featureList]
    body_cut = body[featureList]
    body_cut = pd.to_numeric(body_cut)
    print(testx)
    print(body_cut)
    print(len(body_cut))
    Ypredict = ols_model.predict(body_cut)
    return jsonify({ "prediction": Ypredict[0] })

if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)