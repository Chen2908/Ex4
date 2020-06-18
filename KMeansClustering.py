import chart_studio.plotly as py
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np


class KMeansClustering:
    def __init__(self, file_path):
        self.folder_path = '/'.join(file_path.split('/')[0:-1]) + '/'
        self.data = pd.read_excel(file_path)
        self.grouped_data = pd.DataFrame()

    def check_file(self):
        if self.data.empty or len(self.data.columns) != 16:
            return 'bad input'
        else:
            return 'good input'

    # data pre-processing
    def pre_processing(self):
        self.fill_na()
        self.standardization()
        self.grouped_data = self.group_by_country()
        return 'done'

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
    def group_by_country(self):
        return self.data.groupby('country').mean().drop(columns=['year'])

    def kmeans(self, K, N):
        X = self.grouped_data.values
        kmeans = KMeans(init='random', n_clusters=K, n_init=N).fit(X)
        labels = kmeans.labels_
        self.grouped_data['cluster'] = labels
        # Generosity is y, social_support is x
        fig, ax = plt.subplots()
        sc = ax.scatter(X[:, 2], X[:, 5], c=labels.astype(np.float), edgecolor='k')
        fig.colorbar(sc, ax=ax)

        ax.set_xlabel('Social support', fontsize=12)
        ax.set_ylabel('Generosity', fontsize=12)
        fig.suptitle('K-Means clustering- Generosity as a function of Social support', fontsize=12, fontweight='bold')
        first_path = self.folder_path + 'clusters.png'
        plt.savefig(first_path)
        plt.close(fig)

        countries_data = pd.read_csv('countries_codes.csv')
        countries_dict = dict([(country, code) for country, code in zip(countries_data['Country'].to_numpy(), countries_data['Alpha-3code'].to_numpy())])
        self.grouped_data['country id'] = [countries_dict[x] if x in countries_dict else x for x in self.grouped_data.axes[0]]

        # map
        choro_map = px.choropleth(self.grouped_data, locations="country id", color="cluster",
                                  color_continuous_scale=px.colors.sequential.Aggrnyl, title='K-Means clustering by countries')
        py.sign_in('chengal', 'bXvnMDGbtkb9zqZibQRt')
        second_path = self.folder_path + 'choropleth.png'
        py.image.save_as(choro_map, filename=second_path)
        return first_path, second_path


# filename = 'C:\\Users\\roman\\GitHub\\KMeansClustering\\Dataset.xlsx'
# k = KMeansClustering(filename)
# k.kmeans(3, 10)