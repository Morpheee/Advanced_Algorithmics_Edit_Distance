#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:26:55 2020

@author: bananasacks
"""

"""https://github.com/kennedyCzar/EditDistanceAdvanceAlgoProject/blob/master/dynamicprograms.py
https://stackoverflow.com/questions/10638597/minimum-edit-distance-reconstruction

"""

import numpy as np

#Compute the Edit Distance using Dynamic Programming
##This one gets the optimal alignment edit distance because it switches the strings
def editDistanceDP(str1, str2):
    m = len(str1)
    n = len(str2)
    
#does this part effect run time? #################   
    #if m == 0:
    #    return str2
    #if n == 0:
    #    return str1
    #if n < m:
    #    return editDistanceDP(str2, str1)   
             
    dist_mat = np.zeros([n+1,m+1])
    dist_mat[0,:] = np.arange(0,m+1)
    dist_mat[:,0] = np.arange(0,n+1)
    alignment = np.empty((0,2))

  
    if str1 == str2:
        dictionary = {"ed" : 0 , "alignment" : np.array([["match",str1[j]] for j in range(n)])}
    else:
        for j in range(1,n+1):
            for i in range(1,m+1):
                if str1[i-1] == str2[j-1]: #for a match
                    dist_mat[j,i] = dist_mat[j-1,i-1] #match rowi[j-1])
                else:
                    dist_mat[j,i] = 1+min(dist_mat[j,i-1],dist_mat[j-1,i],dist_mat[j-1,i-1])#min_of(insert, delete, replace) 
        i = m
        j = n
 ##editing string 1
        str1 = ' '+str1
        str2 = ' '+str2
        
        while i!= 0 and j!= 0:
            #edge case
            if i==0 :
                alignment = np.append(["insert",str2[j]],alignment)
                j -= 1
            #edge case
            elif j==0 :
                alignment = np.append(["delete",str1[i]],alignment)
                i -= 1
            #base cases
            else :
                if str1[i]==str2[j]:
                   alignment = np.append(["match",str1[i]],alignment)
                   
                   i -= 1
                   j -= 1
                else:
                   if dist_mat[j,i] == 1+dist_mat[j-1,i]:
                       alignment = np.append(["insert",str2[j]],alignment)
                       j -= 1
                   elif dist_mat[j,i] == 1+dist_mat[j-1,i-1]:
                       alignment = np.append(["replace",str2[j]],alignment)
                       i -= 1
                       j -= 1
                   elif dist_mat[j,i] == 1+dist_mat[j,i-1]:
                       alignment = np.append(["delete",str1[i]],alignment)
                       i -= 1
        dictionary = {"ed" : dist_mat[n,m] , "alignment" : alignment}        

    return(dictionary)

print(editDistanceDP("", "maine"))


    


"""The edit distance working as it should
https://github.com/kennedyCzar/EditDistanceAdvanceAlgoProject/blob/master/DivideandConquer.py

def editDistanceDP(str1, str2):
    m = len(str1)
    n = len(str2)

#does this part effect run time? #################   
    if m == 0:
        return str2
    if n == 0:
        return str1
    if n < m:
        return editDistanceDP(str2, str1)

##################################################    
        
    columnx = [x for x in range(m+1)]
    rowy = [y for y in range(n+1)]
    print(rowy)
    print(columnx)
    if str1 == str2:
        return str1
    else:
        for i in range(1,m+1):
            newY = []
            newY.append(columnx[i])
            for j in range(1,n+1):
                print("i=",i)
                print("j=",j)
                if str1[i-1] == str2[j-1]: #for a match
                    newY.append(rowy[j-1])#match rowi[j-1])
                    print(newY)
                else:
                    newY.append(1+min(newY[-1],rowy[j],rowy[j-1]))#insert, delete, sub 
                    print(newY)   
            rowy = newY
        return newY


#output is []
print(editDistanceDP("man", "maine"))
"""