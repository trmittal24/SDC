import numpy as np
class Node:                                                     # defining the structure of each node in graph
    def __init__(self,initvalue,initlvl,initdata):
        self.data = initdata
        self.value= initvalue
        self.level = initlvl
        self.lchild = None
        self.rchild = None
        self.logic = None
        self.id = None
    def getData(self):                                          # defining basic functions to acquire data
        return self.data
    def getValue(self):
        return self.value
    def getlChild(self):
        return self.lchild
    def getrChild(self):
        return self.rchild
    def getlogic(self):
        return self.logic
    def getId(self):
        return self.id
    def getlvl(self):
        return self.level




    def setData(self,newdata):                                  # defining basic functions to modify data
        self.data = newdata
    def setlChild(self,newdata):
        self.lchild = newdata
    def setrChild(self,newdata):
        self.rchild = newdata
    def setValue(self,newdata):
        self.value = newdata
    def setLogic(self,newdata):
        self.logic = newdata
    def setId(self,newdata):
        self.id = newdata
    def setlvl(self,newdata):
        self.level = newdata
    
class tree:                                                     #data structure for OBDD and ROBDD

    def __init__(self):
        self.head = None
       
    
    def gethead(self):
        return self.head

    def isEmpty(self):
        return self.head == None

    def split(self,node,value,level,array,counter):                                # split function is recursively called till the leaf node 
        if(node.getlChild()!=None):                                                # is reached  
            self.split(node.getlChild(),value,level,array,counter)                 # once it reaches the leaf, left and right children are added      
            self.split(node.getrChild(),value,level,array,counter)
        else:
            
            newNode = Node(value+str(counter[0]),level,array.copy())
            node.setlChild(newNode)
            counter[0] = counter[0] + 1                                            # giving unique labels (like b0,b1,b2...)
        
            newNode2 = Node(value+str(counter[0]),level,array.copy())
            node.setrChild(newNode2)
            counter[0] = counter[0] + 1



    def add(self,value,level,array):                                               # to add a new level
        counter = [0]
        if (self.head == None):                                                    # check if the tree is empty
            newNode = Node(value + str(counter[0]),level,array)
            self.head = newNode                                                    # make the new node the head
        else:                                                                      # else call spilt to add level              

            self.split(self.head,value,level,array,counter)

    def callshow(self,dot):                                                        # contructs the OBDD graph in "dot" format          
        if(self.head!=None):
            self.show(self.head,dot)

    def show(self,node,dot):                                                       # recursively called function to create "dot" graph
        if(node != None):
            if(node.getlogic() != None ):
                dot.node(node.getValue(),str(node.getlogic()), shape = 'box')      # use a "box", if leaf node and display logic
            else:
                dot.node(node.getValue(),node.getValue()[:-1])                     # display variable(like a,b)  
            if(node.getlChild() != None):
                dot.edge(node.getValue(),node.getlChild().getValue(),'0')          # create an edge between nodes with logic ( 0 or 1 ) on edge 
                dot.edge(node.getValue(),node.getrChild().getValue(),'1')

            self.show(node.getlChild(),dot)                                        # recursively call itself
            self.show(node.getrChild(),dot)

    def callshow_robdd(self, dot):                                                 # contructs the ROBDD graph in "dot" format                                          
        if(self.head!=None):
            self.show_robdd(self.head, dot)

    def show_robdd(self,node,dot):                                                 # similar to show function

        if(node != None):
            if(node.getlogic() != None ):
                dot.node(str(node.getId()),str(node.getlogic()), shape = 'box')
            else:
                dot.node(str(node.getId()),node.getValue()[:-1])

            if(node.getlChild() != None):
                dot.edge(str(node.getId()),str(node.getlChild().getId()),'0')

                dot.edge(str(node.getId()),str(node.getrChild().getId()),'1')
                        
            self.show_robdd(node.getlChild(),dot)
            self.show_robdd(node.getrChild(),dot)

    def apply(self):
        if(self.head != None):
            self.appl(self.head.getlChild(),0)
            self.appr(self.head.getrChild(),0)
        else:
            print("tree is empty")

#the functions childdatachangel,childdatachangel,appl,appr are recursively called to change the PCN  
#values of each node depending on the level and position i.e left or right 

    def childdatachangel(self,node,index):
        if(node!=None):
            temp = node.getData()
            for x in range(0, len(temp)):
                if(temp[x][index]=='01'):
                    temp[x][index] = '00'
                if(temp[x][index]=='10'):
                    temp[x][index] = '11'
            node.setData(temp)
            self.childdatachangel(node.getlChild(),index)
            self.childdatachangel(node.getrChild(),index)

    def childdatachanger(self,node,index):                              # works in conjunction with "apply"
        if(node!=None):
            temp = node.getData()
            for x in range(0, len(temp)):
                if(temp[x][index]=='01'):
                    temp[x][index] = '11'
                if(temp[x][index]=='10'):
                    temp[x][index] = '00'
            node.setData(temp)
            self.childdatachanger(node.getlChild(),index)
            self.childdatachanger(node.getrChild(),index)


    def appl(self,node,index):                                          # works in conjunction with "apply"
        if(node!= None):

            temp = node.getData()

            for x in range(0, len(temp)):
                if(temp[x][index]=='01'):
                    temp[x][index] = '00'
                if(temp[x][index]=='10'):
                    temp[x][index] = '11'
            node.setData(temp)
            self.childdatachangel(node.getlChild(),index)
            self.childdatachangel(node.getrChild(),index)

            
            self.appl(node.getlChild(),index+1)
            self.appr(node.getrChild(),index+1)

    def appr(self,node,index):                                          # works in conjunction with "apply"
        if(node!= None):
            temp = node.getData()
            
            for x in range(0, len(temp)):
                if(temp[x][index]=='01'):
                    temp[x][index] = '11'
                if(temp[x][index]=='10'):
                    temp[x][index] = '00'
            node.setData(temp)
            self.childdatachanger(node.getlChild(),index)
            self.childdatachanger(node.getrChild(),index)

            self.appl(node.getlChild(),index+1)
            self.appr(node.getrChild(),index+1)

    def setfinal(self,node):    
        if(node != None):
            if 'final' in node.getValue():                               #it sets logic values anf IDs to the leaf nodes  
                finalcheck = 0
                for x in node.getData():
                    check = 1
                    for y in x:
                        if y == '00':
                            check = 0
                            break
                    if(check == 1):
                        finalcheck = 1
                if(finalcheck == 1):
                    node.setLogic(1)
                    node.setId(2)
                else:
                    node.setLogic(0)
                    node.setId(1)

            self.setfinal(node.getlChild())
            self.setfinal(node.getrChild())
    
    def firstloop(self,height):                                         # starts the process to assign IDs level by level
        checkarray = []
        for i in reversed(range(height)):
        
            self.idsetting(self.head,i,checkarray)
        

    def idsetting(self,node,level,checkarray):
        if(node != None):
            self.idsetting(node.getlChild(),level,checkarray)
            self.idsetting(node.getrChild(),level,checkarray)

            if(node.getlvl() == level):                         
                    left = node.getlChild().getId()
                    right = node.getrChild().getId()
                    if(left == right):                                  #nodes with same left and right children are given the same ID as them
                        sum = left
                        node.setLogic(node.getlChild().getlogic())      #the value of the children is copied into the parent and they 
                        node.setValue(node.getlChild().getValue())      #are set to none
                        node.setlChild(None)
                        node.setrChild(None)
                    else:
                        sum = left + right
                        sum = self.checkarr(checkarray,sum,left,right)  #else the ID is set as the sum of the IDs of the two children
                    node.setId(sum)                                     #provided this value is not already assigned as an ID previously 
                    checkarray.append([sum, left, right])

    def checkarr(self, checkarray,sum,left,right):                      # checks if ID to be assigned has not been used previously
        for x in checkarray:
            if (sum == x[0]):
                if (left != x[1] or right != x[2]):
                    final = self.checkarr(checkarray,sum+1,left,right)
                    return final
        return sum
        return sum

    def ite(self, node):
        if(node.getlogic() == 1 or node.getlogic() == 0):               # check if we have reached leaf node
            print ( str(node.getlogic()) + ',' , end = '')              # print node logic ( 0 or 1)       
            return node.getlogic()

        print ("ite ( " + str(node.getValue()[:-1]) + ',', end = '')    # print the node variable

        self.ite(node.getrChild())                                      # recursively iterate: 1) right child              
        self.ite(node.getlChild())                                      #                      2) left child 

        print (')', end = '')

