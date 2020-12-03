#! /usr/bin/env python3
import numpy as np

def mat_dp_ed(x,y) :
	"""
Parameters :
	x,y : strings.
Return :
	l[1,:] : the last line of the array created by the dynamic programming approach.
	"""
	#add blank space at the beginning of each words.
	#correspond to row 0 and column 0 of the array.
	x=' '+x
	y=' '+y

	#n and m correspond to len(x) and len(y) for easier reading.
	n=len(x)
	m=len(y)

	#initialize the array.
	l=np.zeros(shape=(m,n),dtype=int)
	l[0,:]=np.arange(n)
	l[:,0]=np.arange(m)

	#main loop of the function.
	for i in range(1,m) :
		for j in range(1,n) :
			if x[j] == y[i] :
				#copy paste the number from the upper-left cell if (letter j if x == letter i if y)
				l[i,j] = l[i-1,j-1]
			else :
				#else take the min value +1 between upper, left, or upper-left cell
				l[i,j] = min(	l[i-1, j ] ,
								l[i-1,j-1] ,
								l[ i ,j-1] )+1 
	return l

def backward_mat_dp_ed(x,y) :
	"""
Parameters :
	x,y : strings.
Return :
	r[0,:] : the first line of the array created by the backward dynamic programming approach.
	"""
	#add blank space at the beginning of each words.
	#correspond to row 0 and column 0 of the array.
	x=' '+x
	y=' '+y

	#n and m correspond to len(x) and len(y) for easier reading.
	n=len(x)
	m=len(y)

	#initialize the array.
	r=np.zeros(shape=(m,n),dtype=int)
	r[m-1,:]=np.arange(n-1,-1,-1)
	r[:,n-1]=np.arange(m-1,-1,-1)

	#main loop of the function.
	for i in range(m-2 , -1,-1) :
		for j in range(n-2, -1 , -1) :
			if x[j+1] == y[i+1] :
				#copy paste the number from the lower-right cell if (letter j+1 if x == letter i+1 if y)
				r[i,j] = r[i+1,j+1]
			else :
				#else take the min value +1 between lower, right, or lower-right cell
				r[i,j] = min(	r[i+1, j ] ,
								r[i+1,j+1] ,
								r[ i ,j+1] )+1
	return r

def ed_dp(x='',y='') :
	'''
Parameters :
	x,y : strings
Return :
	ed : integer, optimal edit distance between x and y.
	alignment : array of instructions, to go from y to x.
	'''

	sum_mat = mat_dp_ed(x,y) + backward_mat_dp_ed(x,y)


	i = len(x)
	j = len(y)

	alignement = np.empty(shape = (0,2))

	while i>0 or j>0 :
		if i==0 :
			alignement = np.append([['add',x[i-1]]],alignement,axis=0)
			j -= 1
		elif j==0 :
			alignement = np.append([['del',y[j-1]]],alignement,axis=0)
			i -= 1
		else :
			if sum_mat[j,i] == sum_mat[j-1,i-1] and x[i-1]==y[j-1] :
				alignement = np.append([['skip',y[j-1]]],alignement,axis=0)
				i-=1
				j-=1
			elif sum_mat[j,i] == sum_mat[j-1,i-1] :
				alignement = np.append([['sub',x[i-1]]],alignement,axis=0)
				i-=1
				j-=1
			elif sum_mat[j,i] == sum_mat[j-1,i] :
				alignement = np.append([['del',y[j-1]]],alignement,axis=0)
				j-=1
			else : #sum_mat[i,j] == sum_mat[i,j-1] :
				alignement = np.append([['add',x[i-1]]],alignement,axis=0)
				i-=1
	return {"ed" : sum_mat[0,0], "alignment" : alignement}



if __name__ == "__main__" :
	x = 'HELLO'
	y = 'HOLA'
	print(ed_dp(x,y))
