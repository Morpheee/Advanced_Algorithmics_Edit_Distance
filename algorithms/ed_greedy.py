#! /usr/bin/env python3

import numpy as np

def greedy_distance(str1,str2) :
    n=len(str1)
    ed = 0
    alignement = np.empty((0,2))

    for i in range(n) :
        if str1[i] == str2[i] :
            alignement = np.append(alignement,[[ 'skip',str1[i] ]] , axis=0)
        elif str1[i] == "-" :
            alignement = np.append(alignement,[[ 'add',str2[i] ]] , axis=0)
            ed+=1
        elif str2[i] == "-" :
            alignement = np.append(alignement,[[ 'del',str1[i] ]] , axis=0)
            ed+=1
        else : #str1[i] != #str2[i]
            alignement = np.append(alignement,[[ 'sub',str1[i] ]] , axis=0)
            ed+=1

    return {"ed" : ed , "alignement" : alignement}


        

def edit_distance_greedy(x='', y='') :

    y_bigger = False
    if len(x) < len(y) :
        x,y=y,x
        y_bigger = True

    n=len(x)
    m=len(y)
    
    ed_align = {"ed" : len(x) , "alignement" : np.array( [["sub",x[i]] for i in range(m)] + [["del",x[i+m]] for i in range(n-m)] ) }

    for i in range( 1 , min(n-m , int(m/2)+1)+1 ) :
        w_1 = i*"-" +x
        w_2 = y+ (i + n-m)*"-"
        new_ed_align = greedy_distance(w_1,w_2)
        if new_ed_align["ed"] < ed_align["ed"] :
            ed_align = new_ed_align

    for i in range( 1 , min(n-m , int(m/2)+1)+1 ) :
        w_1 = x+ i*"-"
        w_2 = (i + n-m)*"-" +y
        new_ed_align = greedy_distance(w_1,w_2)
        if new_ed_align["ed"] < ed_align["ed"] :
            ed_align = new_ed_align

    for i in range( (n-m)+1 ) :
        w_1 = x
        w_2 = (n-m-i)*"-" +y+ (i)*"-"
        new_ed_align = greedy_distance(w_1,w_2)
        if new_ed_align["ed"] < ed_align["ed"] :
            ed_align = new_ed_align
    return ed_align

#print(edit_distance_greedy( x="ABC" , y="BCFGHIJK" ))