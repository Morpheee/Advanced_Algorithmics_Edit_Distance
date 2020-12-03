 #recursion for Edit Distance
def RecED(s1,s2,operations=[],ED=0):
    if len (s1)==0:
        return ED+len(s2),operations+ [{'insert':x} for x in s2 ]  
    if len(s2)==0:
        return ED+len(s1),operations+ [{'insert':x} for x in s1 ] 
    if(s1[-1]== s2[-1]):
        k = 0
        w1=RecED(s1[:-1],s2[:-1],operations+[{'skip':s1[-1]}],ED+k)
    else:
        k = 1
        w1=RecED(s1[:-1],s2[:-1],operations+[{'replace':s1[-1]}],ED+k)
        
    w2=RecED(s1[:-1],s2,operations+[{'delete':s1[-1]}],ED+1)
    w3=RecED(s1, s2[:-1],operations+[{'insert':s2[-1]}],ED+1) 
    if w1[0]<=w2[0] and w1[0]<=w3[0]:
        return w1
    elif w2[0]<=w1[0] and w2[0]<=w3[0]:
        return w2  
    else :
        return w3