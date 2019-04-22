import os
import pandas as pd

from flask import Flask, request, jsonify
from flask_cors import CORS
from services import star_predict as stars
from services import ols_stars_local
from services import knn
from services import gh_api
from services import plots

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def _predict_mock_data():
    # Fill NaN with None (which converts to null) since that will f up our JSON
    # because DataFrame.to_dict can't do it for us
    repo_df = gh_api.get_test_data()
    repo_df = repo_df.where((pd.notnull(repo_df)), None)
    
    as_dict = repo_df.to_dict(orient='records')[0]
    r_prediction = stars.predict_dict(as_dict)

    return r_prediction


@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = gh_api.get_test_data()

    sns_path = plots.create_sns_plot(projects)
    
    return projects.to_json(orient='./' + f_name + '.png''records')


@app.route('/api/projects/predict', methods=['POST'])
def get_predicted_project():
    body = request.get_json()
    if 'nameWithOwner' not in body:
        return 'nameWithOwner missing from JSON', 400
    
    name = body['nameWithOwner']

    repo_dict = {}

    try:
        # K-nn
        computed_knn = knn.compute_knn(name)

        # Star-prediction
        repo_dict = gh_api.find_repo_by_fullname_as_dict(name)
        # predicted_stars = _predict_mock_data()
        predicted_stars = stars.predict_dict(repo_dict) 

        repo_dict['predicted_stars'] = predicted_stars
        repo_dict['knn_distances'] = computed_knn[0].tolist()
        repo_dict['knn_names'] = computed_knn[1].tolist()

        return jsonify(repo_dict)
    except OSError as e:
        print(e)
        if (e.errno == 2):
            return 'Pickle file containing the model not found', 500
        else:
            return 'Something went wrong ¯\\_(ツ)_/¯', 500
    except Exception as e:
        print(e)
        return 'Something went wrong ¯\\_(ツ)_/¯', 500

if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)