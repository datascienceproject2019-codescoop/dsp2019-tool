import seaborn as sns 
import pandas as pd 
import os
import io
from pandas.core.frame import DataFrame

images_folder = 'resources/images'

def create_image_folder():
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)


def create_sns_plot(frame: DataFrame) -> str:
    """
    Returns path from where the plot is accessable
    """
    create_image_folder()
    full_path = images_folder + '/sns.png'

    if not os.path.isfile(full_path):
        print('Generating new SNS plot png')
        plt = sns.pairplot(frame)
        plt.fig.suptitle("Features Comparison", y = 1.00, fontsize=18)
        plt.savefig(full_path)

    return full_path
    

def create_issues_stars_plot(frame: DataFrame) -> str:
    create_image_folder()
    full_path = images_folder + '/issueStar.png'

    if not os.path.isfile(full_path):
        print('Generating new \'issues vs stars\' plot png')
        issues_plot = sns.pairplot(frame)
        issues_plot.fig.suptitle("Issues vs Stars", y = 1.0, fontsize=18)
        issues_plot.savefig(full_path)

    return full_path


def image_to_bytes(path: str):
    byte_io = io.BytesIO()

    with open(path, 'rb') as image:
        byte_io.write(image.read())
        byte_io.seek(0)

    return byte_io
