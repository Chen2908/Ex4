import plotly
import pandas as pd
from sklearn.preprocessing import StandardScaler


class KMeansClustering:
    def __init__(self, file_name):
        self.data = pd.read_excel(file_name)
        # data pre-processing
        self.fill_na()
        self.standardization()
        self.grouped_data = self.group_by_county()

    # fill na value of numeric columns with their mean
    def fill_na(self):
        for col in self.data.columns:
            if col != 'country' and col != 'year':
                self.data[col].fillna(self.data[col].mean(), inplace=True)

    # standardize numeric columns
    def standardization(self):
        for col in self.data.columns:
            if col != 'country' and col != 'year':
                self.data[[col]] = StandardScaler().fit_transform(self.data[[col]])

    # group all rows with the same country into one with mean values
    def group_by_county(self):
        return self.data.groupby('country').mean().drop(columns=['year'])


filename = 'Dataset.xlsx'
KMeansClustering(filename)
