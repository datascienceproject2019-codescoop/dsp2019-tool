import seaborn as sns 
import pandas as pd 
import os
from pandas.core.frame import DataFrame

def create_sns_plot(frame: DataFrame) -> str:
    file_path = './resources/sns.png'

    if not os.path.isfile(file_path):
        print('Generating new SNS plot png')
        image_frame = frame[['Contributors Count', 'Forks Count', 'Watchers Count', 'Stars Count']]
        plt = sns.pairplot(image_frame)
        plt.savefig(file_path)

    return file_path
    