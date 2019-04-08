from flask import Flask, request, jsonify
from flask_cors import CORS
from services import star_predict as stars
from services import knn
from services import gh_api

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def _get_gh_repo_by_name(name: str):
    """
    Returns json turned into dictionary. Gathers several API-calls to produce 
    required fields for star prediction
    """

    repos = gh_api.find_repositories_by_fullname(name)

    for i, repo in enumerate(repos): 
        langs = gh_api.find_langs_by_fullname(repo['full_name'])
        repos[i] = {**repo, **langs}

        repos[i]['Contributors Count'] = gh_api.count_items_by_link(repo['contributors_url'])
        repos[i]['Open Issues Count'] = gh_api.get_open_issues_by_fullname(repo['full_name'])['total_count']
        repos[i]['Default branch'] = gh_api.get_branch_index(repo['branches_url'], repo['default_branch'])
    
    return repos


def _predict_mock_data(repo_df, predictions):
    as_dict = repo_df.to_dict(orient='records')[0]
    r_prediction = stars.predict_stars(as_dict)
    r_name = as_dict['Name with Owner'][0]
    
    predictions.append({ 'name': r_name, 'prediction': r_prediction })

    return predictions


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

    predicted_stars = []

    repos = _get_gh_repo_by_name(name)

    if len(repos) == 0:
        return 'No project found with given name "{}"'.format(name), 404
    if len(repos) > 1:
        return 'Somehow you managed to find multiple projects with the same name "{}" and break me :('.format(name), 400

    repo = repos[0]

    try:
        predicted_stars = stars.predict_gh_data(repo)
        computed_knn = knn.compute_knn(name)

        repo['predicted_stars'] = predicted_stars
        repo['knn_distances'] = computed_knn[0].tolist()
        repo['knn_nearest'] = computed_knn[1].tolist()

        return jsonify(repo)
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