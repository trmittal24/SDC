import collections #libraray used for ordered dictionaries

x=0 
file=open("table.txt","r")#reading input from file
input1=file.readlines()
countOnes={}
flaggedRows={k: 0 for k in range(len(input1))}


for i in range(len(input1)) :
    input1[i]=list(input1[i][:-1])  #parsing data in required format
    size=len(input1[i])



flaggedColumns={k: 0 for k in range(len(input1[0]))}

output = [0 for y in range(size)]
for i in range(len(input1)):
	if (flaggedRows[i] !=1):
		counter=0
		for j in range (len(input1[i])):
			if(flaggedColumns[j] != 1):
				if input1[i][j] == '1':
					counter +=1
					index=j
		countOnes[i] = counter #counts number of ones in each column(ignores all flagged Rows)
		if counter==1:
			flaggedRows[i]=1 
			x+=1
			flaggedColumns[index]=1
			output[index]=1

			for j in range(len(input1)):
				if(input1[j][index]== '1'):
					flaggedRows[j] = 1	
					x+=1

	
columnOnes={}
while (sum(flaggedRows.values())!=len(input1)):
	for i in range(len(input1[0])):
		if (flaggedColumns[i] != 1):
			counter=0
			for j in range(len(input1)):
				if (flaggedRows[j]!=1):
					if(input1[j][i]=='1'):
						counter +=1
			columnOnes[i]=counter

	sortedC = collections.OrderedDict(sorted(columnOnes.items(), key=lambda x:x[1], reverse=True))
	# this creates a sorted dictionary in which the key(column_number) is mapped to number of ones in that column
	value = list(sortedC.values())[0]
	inv_map = {v: k for k, v in sortedC.items()}
	flaggedColumns[inv_map[value]]=1
	output[inv_map[value]]=1 # the corresponding column index of output is marked as one
	#(this implies that particular minterm is a part of the minimum cover) 
	columnOnes[inv_map[value]]=0
	
	for f in range(len(input1)):
		if (input1[f][inv_map[value]]=='1'):
			flaggedRows[f]=1
			x+=1
print("The mimimum cover is given by:" + str(output))
