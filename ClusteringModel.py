import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from sklearn.cluster import KMeans
from transformers import AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from hazm import *


class Cluster:
    def __init__(self):
        self.num_of_clusters = 17
    def preproccess(self,pathOfFile,columnName):
        data = pd.read_excel(pathOfFile)
        data = data[columnName]
        data.dropna(inplace=True)
        data.drop_duplicates(keep='first', inplace=True)
        dataList = self.cleanData(data.copy())
        embeddings = self.createEmbeddings(dataList)
        return embeddings,data.values.tolist()

    def cleanData(self,data):
        hazm_tokenizer = WordTokenizer(replace_numbers=True, replace_ids=True)
        hazm_stemmer = Stemmer()
        hazm_lemmatizer = Lemmatizer()
        stopwords = stopwords_list()
        #Tokenizing data
        data = data.apply(lambda v: hazm_tokenizer.tokenize(v))
        print(data.head())

        #Remove stop words
        data = data.apply(lambda v: [w for w in v if w not in stopwords])
        print(data.head())

        #Joining words
        data = data.apply(lambda v: ' '.join(v))
        print(data.head())
        return list(data)

    def createEmbeddings(self,data):
        # Initialize the model for creating embeddings
        model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
        embeddings = np.array(model.encode(data, task="text-matching")) #Length of each embed is 1024
        return embeddings

    def predictKmeans(self,embeddings):
        km = KMeans()
        km = KMeans(n_clusters=self.num_of_clusters,
        init='k-means++')
        self.y_km = km.fit_predict(embeddings)
        return km

    def extractClustersContent(self):
        for i, centroid in enumerate(self.model.cluster_centers_):
            similarities = cosine_similarity([centroid], self.embeddings)[0]
            closest_doc_idx = similarities.argmax()
            print(f"Representative document for Cluster {i}:")
            print(self.dataList[closest_doc_idx])
        clusters = dict()
        #Extract first 10 text for each cluster
        for label in np.unique(self.model.labels_):
            indices = np.where(self.model.labels_ == label)[0][:10]
            cluster_elements = np.array(self.dataList)[indices]
            print(f"Cluster {label} elements:")
            print(cluster_elements)
            clusters[f"{label}"] = cluster_elements.tolist()
        return json.dumps(clusters,ensure_ascii=False)
    
    def plotClusters(self):
        pca = PCA(n_components=3)
        reduced_embeddings = pca.fit_transform(self.embeddings)
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        colors = ["r", "g", "b", "y", "c", "m"]
        for i in range(self.num_of_clusters):
            ax.scatter(
            reduced_embeddings[self.y_km == i, 0] ,
            reduced_embeddings[self.y_km == i, 1] ,
            reduced_embeddings[self.y_km == i, 2] ,
            label=f"cluster:{i}",
            color=colors[i % len(colors)])
        plt.show()

    def predict(self,pathOfExcelFile,columnName):
        self.embeddings,self.dataList = self.preproccess(pathOfExcelFile,columnName)
        self.model = self.predictKmeans(self.embeddings)