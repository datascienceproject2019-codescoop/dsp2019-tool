from flask import Flask, request, jsonify
from flask_cors import CORS
from services import star_predict as stars
from services import gh_api

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = gh_api.get_projects()
    return projects.to_json(orient='records')


@app.route('/api/projects/predict', methods=['POST'])
def get_predicted_project():
    body = request.get_json()
    if 'nameWithOwner' not in body:
        return 'nameWithOwner missing from JSON', 400
    
    name = body['nameWithOwner']

    repos = gh_api.find_repos_by_name(name)

    predicted_stars = []

    try:
        for r in repos:
            as_dict = r.to_dict(orient='records')[0]

            r_prediction = stars.predict_stars(as_dict)
            r_name = as_dict['Name with Owner'][0]
            
            predicted_stars.append({ 'name': r_name, 'prediction': r_prediction })

        return jsonify({ 'predictions': predicted_stars })
    except OSError as e:
        print(e)
        if (e.errno == 2):
            return 'Pickle file containing the model not found', 500
        else:
            return 'Something went wrong ¯\\_(ツ)_/¯', 500


@app.route('/api/stars/predict', methods=['POST'])
def ols_predict():
    json_dict = request.get_json()

    try:
        predicted_stars = stars.predict_stars(json_dict)

        return jsonify({ 'prediction': predicted_stars })
    except OSError as e:
        print(e)
        if (e.errno == 2):
            return 'Pickle file containing the model not found', 500
        else:
            return 'Something went wrong ¯\\_(ツ)_/¯', 500


if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)