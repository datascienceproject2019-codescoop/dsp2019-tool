from flask import Flask, request, jsonify
from flask_cors import CORS
from services import star_predict as stars
import pickle
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

def load_ols_model():
    with open('models/pickle_model', 'rb') as pmodel:  
        pickle_model = pickle.load(pmodel)
        return pickle_model

test500 = pd.read_csv('data500.csv')
ols_model = load_ols_model()

# Hard-coded list of features our model deems are most important
featureList = ['Java', 'Pages enabled', 'Issues enabled', 'Scala', 'PHP',
        'Python', 'Default branch', 'Size', 'Contributors Count',
        'Forks Count', 'Open Issues Count', 'Watchers Count', 'Emacs Lisp',
        'BSD-2-Clause', 'JavaScript', 'Wiki enabled', 'MIT',
        'Pull requests enabled', 'Fork', 'HTML', 'Other', 'CSS', 'Go',
        'Shell', 'Objective-C']

@app.route('/api/projects', methods=['GET'])
def get_projects():
    return test500.to_json(orient='records')

@app.route('/api/projects/predict', methods=['POST'])
def get_predicted_project():
    body = request.get_json()
    if 'nameWithOwner' not in body:
        return 'nameWithOwner missing from JSON', 400
    
    name = body['nameWithOwner']
    found = test500.loc[test500['Name with Owner'] == name]

    if len(found) == 0:
        return 'No project found with given name "{}"'.format(name), 404
    if len(found) != 1:
        return 'Somehow you managed to find multiple projects with the same name "{}" and break me :('.format(name), 400

    predicted_stars_thingy = ols_model.predict(found[featureList])
    found.insert(0, 'predicted_stars', predicted_stars_thingy)
    # Records turns the dataframe into a list of things, lines as line-delimited JSON (not a list)
    return found.to_json(orient='records', lines=True)

@app.route('/api/stars/predict', methods=['POST'])
def ols_predict():
    json_dict = request.get_json()

    try:
        predicted_stars = stars.predict_stars(json_dict)

        return jsonify({ "prediction": predicted_stars })
    except OSError as e:
        print(e)
        if (e.errno == 2):
            return 'Pickle file containing the model not found', 500
        else:
            return 'Something went wrong ¯\\_(ツ)_/¯', 500


if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)