import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class DataPipeLine :

    def __init__(self, data_source):
        self.data_path = data_source
        self.data = None
        self.scaled_data = None
        self.pca_data = None

    def load_data(self):
        self.data = pd.read_csv(self.data_path)

    def scale_data(self):
        scaler = StandardScaler()
        self.scaled_data = scaler.fit_transform(self.data)

    def perform_pca(self, n_components):
        pca = PCA(n_components=n_components)
        self.pca_data = pca.fit_transform(self.scaled_data)

    def run_pipeline(self, n_components):
        self.load_data()
        self.scale_data()
        self.perform_pca(n_components)

