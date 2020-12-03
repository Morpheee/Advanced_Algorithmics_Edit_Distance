#! /usr/bin/env python3
import numpy as np

def concat(p,q) :
	'''
Parameter :
	p,q : array, sorted* countaining the points of interest.
Return :
	p : array, concatenation of p and q.
The concatenation is such that p is sorted*.
Also the point in p are optimal, in the way that there is no point sharing a coordinate, 
and the points have the smallest second coordinate possible.

* : sorted here is regarding the first then second coordinate of each point.
	'''
	#two edge cases, if p is empty, if q is empty
	if p == [] :
		return q
	elif q == [] :
		return p
	else :
		j = 0
		add_tail_of_q = False #must not add the tail of q
		for i in range(len(q)) :
			while p[j][0] < q[i][0] :
				j += 1
				if j == len(p) :
					add_tail_of_q = True #all remaining points of q are bigger than the points of p so add the tail of q in p
					break
			if add_tail_of_q :
				p = p + q[i:]
				break
			else :
				if p[j][0] == q[i][0] : 
					if p[j][1] > q[i][1] :
						p[j] = q[i] #the points are : p[j]:=(a,b), q[i]:=(a,c) with b>c so must replace p[j] by q[i]
						break
				else :
					p = p[:j] + [q[i]] + p[j:] #p[j]:=(a,b), p[j+1]:=(a',b'), q[i]=(c,d) and a<c<a' so must add q[i] in between p
					j += 1
	return p

def space_efficient_dp_ed(x,y) :
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
	l=np.zeros((2,n),dtype=int)
	l[0,:]=np.arange(n)
	l[1,0]=1

	#main loop of the function.
	for i in range(1,m) :
		for j in range(0 if i>1 else 1,n) :
			if j>0 :
				if x[j] == y[i] :
					#copy paste the number from the upper-left cell if (letter j if x == letter i if y)
					l[1,j] = l[0,j-1]
				else :
					#else take the min value +1 between upper, left, or upper-left cell
					l[1,j] = min(	l[0 , j] ,
									l[0,j-1] ,
									l[1,j-1] )+1 
			else :
				#else case : the current cell is the most left one. (in this case it must be equal to the upper cell +1)
				l[1,j] = l[0,j]+1
		#make the first row of the array equal to the second one. (As the array is space efficient, it only uses two rows).
		l[0,:] = l[1,:]
	return l[1,:]

def backward_space_efficient_dp_ed(x,y) :
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
	r=np.zeros((2,n),dtype=int)
	r[1,:]=np.arange(n-1,-1,-1)
	r[0,n-1]=1

	#main loop of the function.
	for i in range(m-2 , -1,-1) :
		for j in range(n-1 if i<m-2 else n-2, -1 , -1) :
			if j<n-1 :
				if x[j+1] == y[i+1] :
					#copy paste the number from the lower-right cell if (letter j+1 if x == letter i+1 if y)
					r[0,j] = r[1,j+1]
				else :
					#else take the min value +1 between lower, right, or lower-right cell
					r[0,j] = min(	r[1 , j] ,
									r[1,j+1] ,
									r[0,j+1] )+1
			else :
				#else case : the current cell is the most right one. (in this case it must be equal to the lower cell +1)
				r[0,j] = r[1,j]+1
		#make the second row of the array equal to the first one. (As the array is space efficient, it only uses two rows).
		r[1,:] = r[0,:]
	return r[0,:]


def divide_and_conquer_ed(x='',y='',l_x=0,l_y=0) :
	"""
Parameters :
	x,y : strings, the two words we work with.
	p : records the path for computing the alignement.
	l_x and l_y are the true position -1 of x[0] and y[0] in the original words x and y,
		needed in order to append the absolute value of the path in p in the deeper recursions.
Return :
	{'p' : p, 'ed' : ed} : dictionary containing :
	p : the collection of points of interest to compute the alignment between x and y.
	ed : the edit distance between x and y.
	"""
	def index_minimize_row(row) :
		"""Output the leftest index that minimizes the row."""
		mini=0
		for r in range(1,len(row)) :
			if row[mini] > row[r] :
				mini=r
		return mini

	#initialize n and m
	n=len(x)
	m=len(y)
	#initialize p to empty list
	
	if n < 1 or m < 2 :
		if m == 1 and n > 1 : #edge case, if there is multiple letters in x but 1 in y. Add the index minimizing the row.
			s = space_efficient_dp_ed(x,y) + np.arange(n,-1,-1)
			mini = index_minimize_row(s)
			ed = s[mini] 					#get the edit distance
			p = [(l_x+mini-1 , l_y+m-1)]
		elif n == 1 and m > 0 : #edge case, if there is one letter in x. Add the point corresponding to (x's letter coordinate , lower y's letter coordinate).
			ed = m-1 if x in y else m #if x is in y then there are m-1 operations to do to go from y to x, else there are m changes to do.
			p = [(l_x , l_y)]
		else : #edge case, if at least one of the string is empty.
			if n == 0 and m > 0:
				ed = m
				p = [(0 , m-1)]
			elif n > 0 and m == 0 :
				ed = n
				p = [(n-1 , 0)]
			else : #n == 0 and m == 0
				ed = 0
				p = []
		return dict({'p' : p , 'ed' : ed})

	else :
		l = space_efficient_dp_ed(x,y[:m//2]) 			#call the ed dynamic programming algorithm - top_left to bottom-rigt.
		r = backward_space_efficient_dp_ed(x,y[m//2:]) 	#call the ed dynamic programming algorithm - bottom-rigt to top_left.
		s = l + r 						#sum the two rows

		mini = index_minimize_row(s)	#find the most left index minimizing the sum row.
		ed = s[mini] 					#get the edit distance

		if l_x+mini > 0 : #add the corresponding point to p. In absolute coordinate (regardin the original x and y words).
			p = [(l_x+mini-1 , l_y+m//2-1)]
		else:
			p = []


		#call the algorithm recurcively with left part of x and y, and then with the right parts.
		p = concat(p , divide_and_conquer_ed(x[:mini] , y[:m//2] , l_x = l_x 		, l_y = l_y		)['p']  )	#top-left part of the array
		p = concat(p , divide_and_conquer_ed(x[mini:] , y[m//2:] , l_x = l_x+mini , l_y = l_y+m//2)['p']	)	#bottom-right part of the array

		return dict({'p' : p , 'ed' : ed})

def view_array(x,y,p) :
	'''
Parameters : 
	x,y : strings, the two words.

prints an array view of the alignment between x and y.
	'''
	print(' '.join([' ']+[i for i in x]))
	for i in range(len(y)):
		print(y[i],end='')
		for j in range(len(x)) :
			if (j,i) in p :
				print(' . ',end='')
			else :
				print('  ',end='')
		print('')

def view_alignment(x,y,p,align=np.empty(shape=(0,2))) :
	'''
Parameters : 
	x,y : strings, the two words.
	p : array, collection of point of interest to compute the alignment between x and y.
	align : the already calculated alignment.
Return :
	align : the alignment of x and y with following form : [['X','X'],['-','B'],['-','C'],['A','A'],['A','D']] 
	'''
	if len(x) > 0 and len(y) > 0 :
		if p[0,0] == p[0,1] :
			align = np.append(align,[[x[0],y[0]]], axis=0)
			return view_alignment(x[1:], y[1:], p[1:], align)
		elif p[0,0] > p[0,1] :
			align = np.append(align, [[x[0], '-']], axis=0)
			p[:,0] -= 1
			return view_alignment(x[1:], y, p, align)
		else : #p[0,0] < p[1,0]
			align = np.append(align, [['-', y[0]]], axis=0)
			p[:,1] -= 1
			return view_alignment(x, y[1:], p, align)
			print("\n\n",align)
	elif len(x) == 0 and len(y) > 0 :
		align = np.append(align, [['-', y[0]]], axis=0)
		return view_alignment(x, y[1:], p, align)
	elif len(y) == 0 and len(x) > 0 :
		align = np.append(align, [[x[0], '-']], axis=0)
		return view_alignment(x[1:], y, p, align)
	else : # len(x) == len(y) == 0
	 	return align

def view_operations(x,y,p,oprs=np.empty(shape=(0,2))) :
	'''
Parameters : 
	x,y : strings, the two words.
	p : array, collection of point of interest to compute the alignment between x and y.
	oprs : the already calculated alignment (here on the form of operations).
Return :
	align : the alignment of x and y with following form : [['skip','X'],['del','B'],['del','C'],['skip','A'],['sub','D']]
	'''
	if len(x) > 0 and len(y) > 0 :
		if p[0,0] == p[0,1] :
			if x[0] == y[0] :
				oprs = np.append(oprs,[['skip',y[0]]], axis=0)
			else :
				oprs = np.append(oprs,[['sub',y[0]]], axis=0)
			return view_operations(x[1:], y[1:], p[1:], oprs)
		elif p[0,0] > p[0,1] :
			oprs = np.append(oprs, [['add',x[0]]], axis=0)
			p[:,0] -= 1
			return view_operations(x[1:], y, p, oprs)
		else : #p[0,0] < p[1,0]
			oprs = np.append(oprs, [['del', y[0]]], axis=0)
			p[:,1] -= 1
			return view_operations(x, y[1:], p, oprs)
	elif len(x) == 0 and len(y) > 0 :
		oprs = np.append(oprs, [['del', y[0]]], axis=0)
		return view_operations(x, y[1:], p, oprs)
	elif len(y) == 0 and len(x) > 0 :
		oprs = np.append(oprs, [['add',x[0]]], axis=0)
		return view_operations(x[1:], y, p, oprs)
	else : # len(x) == len(y) == 0
	 	return oprs	

def edit_distance_dnd_dp_linear_space(x='' , y='') :
	'''
edit_distance_dnd_dp_linear_space(x='', y='')
	--> x,y are the strings we want the edit distance and the alignment of.

This algorithm outputs a dictionary :
output {'ed' : 'the optimal Edit Distance between x and y' , 'alignment' : 'an optimal alignment of x and y'}

Space complexity used is linear, it is equal to O(max(len(x),len(y))).
	'''
	p,ed = divide_and_conquer_ed(x,y).values()
	# p = sort_n_clean(p)

	#uncomment next line to see the "array" of the alignment between x and y.
	#view_array(x,y,p)

	#uncomment next line to output the alignment as follow [['X','X'],['-','B'],['-','C'],['A','A'],['A','D']].
	# alignment = view_alignment(x,y,np.array(p))

	#uncomment next line to output the alignment as follow [['skip','X'],['del','B'],['del','C'],['skip','A'],['sub','D']].
	alignment = view_operations(x,y,np.array(p))

	return {'ed' : ed, 'alignment' : alignment}

if __name__ == '__main__' :
	x = 'MAHSLGEQYDLGKPTEEHHESHPPAHQAPHAGGELGA'
	y = 'MAEAQLRDQHGNPVPLTDQYGNPVILTDERGNPVQLT'
	print(edit_distance_dnd_dp_linear_space(x,y))


