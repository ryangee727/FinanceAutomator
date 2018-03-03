import glob
import pandas as pd


class TrainingData(object):
    def __init__(self, data_path):
        self.data_path = data_path
        self.data_frame = self.gather_df_from_path()
        self.training_data_list = self.convert_df_to_training_data()

    def gather_df_from_path(self):
        data_frames = []
        for training_data in glob.glob(self.data_path + '*.csv'):
            data_frames.append(pd.read_csv(training_data, usecols=['Name', 'Category']))
        return pd.concat(data_frames)

    def convert_df_to_training_data(self):
        lst = []
        for index, row in self.data_frame.iterrows():
            lst.append({'cat': row['Category'], 'name': row['Name']})
        return lst

    def get_training_data(self):
        return self.training_data_list

    def get_categories(self):
        return list(set([train_data['cat'] for train_data in self.training_data_list]))