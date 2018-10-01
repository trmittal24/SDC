import numpy as np
import sdctree
from graphviz import Digraph

#Boolean Expressions to Trees
#Code for : 1) robdd--reduced ordered binary decision diagram
# 2) ite

print ("Enter the splitting order:")
order=list(input()) 
numbers = len(order)                  
file=open("input.txt","r")        #complements are represented with capital letters
input1=file.readlines()

for i in range(len(input1)) :
    input1[i]=list(input1[i][:-1])

input1 = np.array(input1,dtype='object')

output = [[0 for y in range(int(numbers))] for x in range(len(input1))]  #initializing the output array


for i in range(len(input1)) :                           # this "for" loop is for converting   
    for j in range(len(order)):                         # alphabets to PCN format
        
        for k in range(len(input1[i])):

            if  order[j] == input1[i][k]:
                output[i][j] = '01'
               
                if(k+1<len(input1[i])):
                    if input1[i][k+1] == "'":
                        output[i][j] = '10'
                break

            if k == len(input1[i])-1:
                output[i][j] = '11' 


output = np.array(output,dtype='object')

dot = Digraph(comment='OBDD')                       #initializing graph for OBDD
dot_robdd = Digraph(comment='ROBDD', strict = True)  #initializing graph for ROBDD
mytree = sdctree.tree()
for counter,x in enumerate(order):
    
    mytree.add(x,counter, output)  #add all the individual nodes
height = counter +1

mytree.add('final',height, output) #add final nodes


mytree.apply()                     #change the cover values 


mytree.setfinal(mytree.gethead())  #sets a 1 or 0 to the final nodes
mytree.callshow(dot)               #display the tree


mytree.firstloop(height)            #call for reduction
mytree.callshow_robdd(dot_robdd)   #display the tree
dot.render('test-output/OBDD', view=True)       #render full
dot_robdd.render('ROBDD', view=True) #render reduced
print ('\n\nITE: \n')
mytree.ite(mytree.gethead())

print ('\n')
