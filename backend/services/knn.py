import pickle
import pandas as pd
import numpy as np

KNN_MODEL_PATH = 'models/knn/knn.pkl'
KNN_DATA_PATH = 'models/knn/knn_data.npy'
KNN_LABELS_PATH = 'models/knn/knn_labels.csv'
REPO_DATA = 'data/repositories-rating.csv'

_knn_model = pickle.load(open(KNN_MODEL_PATH, 'rb'))
_knn_data = np.load(KNN_DATA_PATH)
# Turn Dataframe with a single nameWithOwner column to Series
_knn_labels = pd.read_csv(KNN_LABELS_PATH)
#_scores = pd.read_csv(REPO_DATA)['December 22, 2018']

def compute_knn(nameWithOwner):
    found = _knn_labels[_knn_labels == nameWithOwner]

    if len(found) == 0:
        return np.array([]), np.array([])

    index = found.index[0]
    data_row = np.array(_knn_data[index]).reshape(1, -1)

    distances, indices = _knn_model.kneighbors(data_row)
    # Returns a float np-array and a string np-array of nearest project names
    return distances[0], _knn_labels.iloc[indices[0]].values, 
