#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 11:00:23 2020

@author: Pascalle Banaszek
"""


import os
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
import os
os.chdir("/Users/bananasacks/Desktop/MLDM Python Code/Advanced Algos Project")
from AdvancedAlgorithmsProject_algo import *



#import data from desktop
os.chdir("/Users/bananasacks/Desktop/MLDM Python Code/Advanced Algos Project")
proteins = pd.read_csv("protein_database.csv", header=None)
#proteins.columns={'name','length','group','sequence'})
alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



#print(range(proteins.shape[1])) #gives me range(0,4)

for letter in range(len(alphabet)):
    proteins[alphabet[letter]] = ""
    
    
l = 0    
for column in range(4,len(alphabet)+4):  
    letter = alphabet[l]
    l += 1
    for row in range(0,len(proteins)):      
        sequence = proteins.iloc[row,3]
        proteins.iloc[row, column] = sequence.count(letter)
      

X = proteins.iloc[:, 4:]
y = proteins.iloc[:, 2]   

##K means clustering and printing the chart to show optimal k

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)
plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('')
plt.show()


#Clusters with 3 groups
kmeans = KMeans(n_clusters=3) #
kmeans.fit(X)
labels3 = pd.DataFrame(data = kmeans.labels_, columns = ["labels3"])
protein_cluster = pd.concat([proteins, labels3], axis=1)


#Clusters with 4 groups
kmeans = KMeans(n_clusters=4) #
kmeans.fit(X)
labels4 = pd.DataFrame(data = kmeans.labels_, columns = ["labels4"])
protein_cluster = pd.concat([protein_cluster, labels4], axis=1)

#Outputs to be used to compute the edit distance
protein_cluster.to_csv(r'/Users/bananasacks/Desktop/MLDM Python Code/Advanced Algos Project/protein_cluster.csv', index = False)

#Originally I had these as two separate scripts because the code above took a really long time to run. 
#So I exported the file and imported it again so I don't have to continue to run the code above to each
#time I wanted to analyze the results


protein_cluster = pd.read_csv("protein_cluster.csv")


"""change labels3 or labels4 depending on which group to analyze"""
label = 'labels3'

#Sampling dataset
X_train, X_test, y_train, y_test = train_test_split(
    protein_cluster[['3',label]],
    protein_cluster[label],
    test_size=0.01, #only using 2.5% of the dataset
    random_state=4269,
    stratify=protein_cluster[label]
    )

#print(X_test.head())




#Cartesian product
pair_proteins = X_test.copy()
pair_proteins['key'] = 0

pair_proteins = pair_proteins.merge(pair_proteins, on='key', suffixes={'_1','_2'})

#Drop equal pairs
pair_proteins = pair_proteins[pair_proteins['3_1'] != pair_proteins['3_2']]
pair_proteins.head()


#Calculating edit distance using the backtracking dynamic programming approach
pair_proteins['ed'] = pair_proteins.apply(lambda row: editDistanceDP(row['3_1'],row['3_2'])["ed"], axis=1)
pair_proteins.to_csv(r'/Users/bananasacks/Desktop/MLDM Python Code/Advanced Algos Project/pair_proteins.csv', index = False)



"""change labels3 or labels4 depending on which group to analyze"""
##plotting 3 groups
sns.scatterplot(data = pair_proteins, x = 'labels3_1', y = 'ed')


#Plotting 4 groups
#sns.scatterplot(data = pair_proteins, x = 'labels4_1', y = 'ed')





















