import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# From sklearn.cluster Import kmeans algorithm package.
from sklearn.cluster import KMeans
# From sklearn.metrics Import silhouette_ Score is used to calculate the contour factor.
from sklearn.metrics import silhouette_score

traindata = pd.read_csv('clean_result.csv')

pca = traindata.loc[:, ['times', 'average']]

for i, r in pca.iterrows():
    if r[0] == 1:
        r[1] = 100000000

'''
# The 3 * 2 = 6 subgraphs are divided and mapped in No. 1 subgraph.
plt.subplot(3,2,1)

# Initialize the original data point.
x1 = pca['times']
x2 = pca['average']
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

# The distribution of the original data lattice is made in the No.1 subgraph。
plt.xlabel('times')
plt.ylabel('average')
plt.title('Instances')
plt.scatter(x1, x2)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
markers = ['o', 's', 'D', 'v', '^', 'p', '*', '+']

clusters = [2, 3, 4, 6, 8]
subplot_counter = 1
sc_scores = []
for t in clusters:
    subplot_counter += 1
    plt.subplot(3, 2, subplot_counter)
    kmeans_model = KMeans(n_clusters=t).fit(X)
    for i, l in enumerate(kmeans_model.labels_):
        plt.plot(x1[i], x2[i], color=colors[l], marker=markers[l], ls='None')
    plt.xlabel('times')
    plt.ylabel('average')
    sc_score = silhouette_score(X, kmeans_model.labels_, metric='euclidean')
    sc_scores.append(sc_score)

# Draw the visual display diagram of contour coefficient and the number of different clusters.
    plt.title('K = %s, silhouette coefficient= %0.03f' %(t, sc_score))

# The relationship curve between the contour coefficient and the number of different clusters is drawn.
plt.figure()
plt.plot(clusters, sc_scores, '*-')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Coefficient Score')
plt.show()
'''
#  It is known that dichotomy is the best choice
x1 = np.array(pca['times'])
x2 = np.array(pca['average'])
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b']
markers = ['o', 's', 'D', 'v', '^', 'p', '*', '+']
kmeans_model = KMeans(n_clusters=3).fit(X)
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(x1[i], x2[i], color=colors[l], marker=markers[l], ls='None')
plt.xlabel('times')
plt.ylabel('average')
plt.savefig('kmeans_result.png')
plt.show()
