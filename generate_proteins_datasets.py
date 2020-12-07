import pandas as pd
import numpy as np
import time
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from AdvancedAlgosPascalle import *
from graphviz import Graph

#Import dataset
protein_path = 'protein_dataset'
protein_file = 'export_1603716401.csv'

protein_dataset = pd.read_csv(protein_path+'/'+protein_file)


#Sampling dataset
X_train, X_test, y_train, y_test = train_test_split(
    protein_dataset[['name','protein','group']],
    protein_dataset['group'],
    test_size=0.05,
    random_state=4269,
    stratify=protein_dataset['group']
    )

#Cartesian product
pair_proteins = X_test.copy()
pair_proteins['key'] = 0

pair_proteins = pair_proteins.merge(pair_proteins, on='key', suffixes={'_1','_2'})

#Drop equal pairs
pair_proteins = pair_proteins[pair_proteins['protein_1'] != pair_proteins['protein_2']]


#Generate protein pairs
#lengths = [10,100,1000,2000,5000,10000,20000,50000]
lengths = [10,100,1000,2000,5000]

for n in lengths:
    pair_proteins[['protein_1','protein_2']].head(n).to_csv(protein_path+'/protein_'+str(n)+'.csv', index=False)