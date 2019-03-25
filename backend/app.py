from flask import Flask
import pickle
import pandas as pd

app = Flask(__name__)

featureList = ['Java', 'Pages enabled', 'Issues enabled', 'Scala', 'PHP',
       'Python', 'Default branch', 'Size', 'Contributors Count',
       'Forks Count', 'Open Issues Count', 'Watchers Count', 'Emacs Lisp',
       'BSD-2-Clause', 'JavaScript', 'Wiki enabled', 'MIT',
       'Pull requests enabled', 'Fork', 'HTML', 'Other', 'CSS', 'Go',
       'Shell', 'Objective-C']

@app.route('/')
def hello_world():
    testx = pd.read_csv('testdata.csv')
    testx = testx[featureList]
    with open('models/pickle_model', 'rb') as pmodel:  
        pickle_model = pickle.load(pmodel)

        Ypredict = pickle_model.predict(testx) 

        return Ypredict.to_json()

if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)