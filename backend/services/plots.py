import seaborn as sns 
import pandas as pd 
import os
from pandas.core.frame import DataFrame

images_folder = 'serving_static/static/images'

def create_sns_plot(frame: DataFrame) -> str:
    """
    Returns path from where the plot is accessable
    """

    full_path = images_folder + '/sns.png'
    print(full_path)

    if not os.path.isfile(full_path):
        print('Generating new SNS plot png')
        image_frame = frame[['Contributors Count', 'Forks Count', 'Watchers Count', 'Stars Count']]
        plt = sns.pairplot(image_frame)
        plt.savefig(full_path)

    return full_path
    