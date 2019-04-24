import os
import pandas as pd
import sys
import traceback
import base64
import io

from flask import Flask, request, jsonify, send_file, make_response
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
    
    return projects.to_json(orient='records')


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

        repo_dict['predicted_stars'] = ols_stars_local.predict_stars(name)
        repo_dict['old_predicted_stars'] = stars.predict_dict(repo_dict) 
        repo_dict['knn_distances'] = computed_knn[0].tolist()
        repo_dict['knn_names'] = computed_knn[1].tolist()

        return jsonify(repo_dict)
    except OSError as e:
        print(e)
        print(traceback.format_exc())
        if (e.errno == 2):
            return 'Pickle file containing the model not found', 500
        else:
            return 'Something went wrong ¯\\_(ツ)_/¯', 500
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        return 'Something went wrong ¯\\_(ツ)_/¯', 500


@app.route('/api/images/sns_image', methods=['GET'])
def get_sns_plot_image():
    projects = pd.read_pickle('resources/seaborn_dataframe1.pkl')

    sns_path = plots.create_sns_plot(projects)
    byte_io = plots.image_to_bytes(sns_path)

    response = make_response(send_file(byte_io, mimetype='image/png'))
    response.headers['Content-Transfer-Encoding']='base64'

    return response


@app.route('/api/images/star_issue_image', methods=['GET'])
def get_star_issue_image():
    data = pd.read_pickle('resources/issues_data.pkl')

    plot_path = plots.create_issues_stars_plot(data)
    byte_io = plots.image_to_bytes(plot_path)

    response = make_response(send_file(byte_io, mimetype='image/png'))
    response.headers['Content-Transfer-Encoding']='base64'

    return response


if __name__ == "__main__":
    import os
    app.run(host = '0.0.0.0', port = os.environ.get('PORT'), debug = True)