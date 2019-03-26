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
    body = pd.read_json(request.data, typ='series', dtype=int)
    body_cut = body[featureList] # Pick only features used in the modeling
    body_cut = pd.to_numeric(body_cut) # Convert all string values to ints etc if possible

    # LOL, so what happens here is that the body is a Series object
    # but which in order to convert to DataFrame must be warped with this black
    # magic. Basically we turn the Series.values from 1-d vector to 2-d matrix
    # so that Pandas understands it's a frame with a single row in it.
    body_cut = pd.DataFrame([body_cut.values], index=[0], columns=body_cut.index)
    predicted_stars = ols_model.predict(body_cut)
    return jsonify({ "prediction": predicted_stars[0] })

if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)