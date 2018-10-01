
# coding: utf-8


import itertools

sdc_const = 0.0

# method to fetch MIS of an element 
def fetchMIS(element, MIS_List):
        for i in range(len(MIS_List)):
            if element in MIS_List[i]:
                mis = MIS_List[i][1]
                break
        return mis

# method to fetch sup_list of an element
def fetchSup_list(element, sup_List):
    for i in range(len(sup_List)):
        if element[0] in sup_List[i]:
            sup_list = sup_List[i][1]
            break
    return sup_list
    

####################################### Reading input files ###########################################################
transctions = []
#############Reading input#############################################
with open('input-data.txt') as f:
    content = f.read().splitlines()
    content = [item.replace("{", "") for item in content]
    content = [item.replace("}", "") for item in content]
    content = [item.replace(" ", "") for item in content]
    for line in content:
        transctions.append(line.split(",")) 
f.close()

print(transctions)

i=0
while(i<len(transctions)):
    if transctions[i] == ['']:
        transctions.pop(i)
        i=i-1
    i=i+1


#########READING PARAMETER FILE###################################################################

with open('parameter-file.txt') as f:
    parameterFiles =f.read().split('SDC')
    tempStr = parameterFiles[0].split('\n')
    tempStr1 = parameterFiles[1].split('\n')
    sdc_const = float(str(tempStr1[0].split('=')[1]).strip())
    tempStr.pop()
    for i in range(len(tempStr)):
        tempStr1 = tempStr[i]
        tempStr1 = tempStr1.replace('(','')
        tempStr1 = tempStr1.replace(')','')
        tempStr1 = tempStr1.replace('MIS','')             
        tempStr[i] = tempStr1
    
    
    #added 
    splitItems=[item.split('=') for item in tempStr]
    mis_list={}
    for i in splitItems:
        mis_list[i[0].strip()]= float(i[1].strip())
    
    
    tempStr1 = parameterFiles[1].split('\n')
    sdc_const = float(str(tempStr1[0].split('=')[1]).strip())
    
    cantBeTogetherCandidates = tempStr1[1].split(':')[1].split('}')
        
    must_have = tempStr1[2].split(':')[1].replace(' ', '').split('or')
    
    cannot_be_together = []
    for rTemp in cantBeTogetherCandidates:
        tempCantBeTogether = []
        tempCantBeTogether = rTemp.strip().replace('{','').replace(' ','').strip().split(',')
        if tempCantBeTogether == ['']:
            pass
        else:
            cannot_be_together.append(tempCantBeTogether)
   
f.close()
    
################################# Fetching MIS and Supp List #############################################
sup_list = {}
count = 0
for key in mis_list:
    for transaction in transctions:
        if key in transaction:
                count = count + 1
    sup_list[key] = round(count/len(transctions),5)
    count = 0
    
itm_mis_sup = {}
for key in mis_list:
    itm_mis_sup[key]=[mis_list[key],sup_list[key]]


MIS_List = [ [k,v] for k, v in mis_list.items() ]
sup_List = [ [k,v] for k, v in sup_list.items() ]


####################################### Start #####################################################################

#######################################  Step 1 - Sorting based on MIS ############################################ 

itm_mis_sup_List = [[k,v[0],v[1]] for k, v in itm_mis_sup.items()]
itm_mis_sup_List.sort(key=lambda x: x[1])
print("Minimum Support and Support of Individual Elements")
print(itm_mis_sup_List)

####################################### Step 2 and Step 3: Fetching L_set and F_set ######################################
L_set = []
F_set = []
f1 = []
index = 99

for i in range(len(itm_mis_sup_List)):
    if index == 99:
        if itm_mis_sup_List[i][2] >= itm_mis_sup_List[i][1]:
            index = i
            break

lcombo=[]
for i in range(len(itm_mis_sup_List)):
    if index != 99:
        if itm_mis_sup_List[i][2] >= itm_mis_sup_List[index][1]:
            L_set.append(itm_mis_sup_List[i][0])
            lcombo.append(itm_mis_sup_List[i])

for i in range(len(lcombo)):
    if lcombo[i][2] >= lcombo[i][1]:
        f1.append(lcombo[i][0])            
          
        
i = 0
f1new=[]
nomust = 0

for i in must_have:
    if i is '':
        nomust = 1
if nomust != 1:    
    for i in f1:
        if i in must_have:
            f1new.append(i)
    f1=f1new

f2 = []
    
print("f1 after init pass")
print(f1)
for f1obj in f1:
    count = 0
    for transaction in transctions:
        if f1obj in transaction:
            count = count + 1
    f2.append([f1obj,count])
F_set.append(f2)

####################################### Step 5 - 8 : Candidate generation #########################################
k = 2
ftemp = []
while(k == 2 or len(ftemp) > 1):
    # Candidate Generation where K = 2
    if k == 2:
        c = []
                        
        for j in range(len(itm_mis_sup_List)): #iterating over the combo
            if itm_mis_sup_List[j][0] in L_set: # if item from combo is in L 
                if itm_mis_sup_List[j][2] >= itm_mis_sup_List[j][1]:# count > mis
                    for i in range(j+1, len(itm_mis_sup_List)):     #generate possible sets 
                        if itm_mis_sup_List[i][2] >= itm_mis_sup_List[j][1] and abs(itm_mis_sup_List[i][2] - itm_mis_sup_List[j][2]) <= sdc_const:
                            temp = [] # the sets are valid only when count(2nd item) > mis(1st item)
                            temp.append(itm_mis_sup_List[j][0])
                            temp.append(itm_mis_sup_List[i][0])
                            c.append(temp)
    else:
	# Candidate Generation where K > 2
        c = []
        fjointemp = []
        for i in range(len(ftemp)):
            #Fetch List - End Element from List
            f1 = ftemp[i][0:(len(ftemp[i])-1)]
            for j in range(i+1, len(ftemp)):
                #Fetch List - End Element from List
                f2 = ftemp[j][0:(len(ftemp[j])-1)]
                #Check if suitable for joining
                if f1 == f2 and abs(fetchSup_list(ftemp[j][(len(ftemp[j])-1):], sup_List) - fetchSup_list(ftemp[i][(len(ftemp[i])-1):], sup_List)) <= sdc_const:
                    fjointemp = ftemp[i] + ftemp[j][(len(ftemp[j])-1):]
                    c.append(fjointemp)
                    fjointemp = []
        i = 0
        while i < len(c):
            subsetlist = list(set(itertools.combinations(c[i], len(c[i])-1)))
            for subset in subsetlist:
                if (c[i][0] in subset) or (fetchMIS(c[i][0], MIS_List) == fetchMIS(c[i][1], MIS_List)):
                    ftcounter = 0
                    for ft in ftemp:
                        if list(subset) == list(ft):
                            ftcounter = ftcounter + 1
                            break
                    if ftcounter == 0:
                        c.pop(i)
                        i = i - 1
                        break
                if i == len(c):
                    break
            i = i + 1
			
 ####################################### Generating Frequent Set ##################################################     
    count = 0
    mis = 0
    ftemp = []
    fprune = []
    F_set_withFrequency = []
    ffinal = []
    for cg in c:
        for transaction in transctions:
            if set(cg) <= set(transaction):
                count = count + 1
        for i in range(len(MIS_List)):
            if cg[0] in MIS_List[i]:
                mis = MIS_List[i][1]
                break
        if count/len(transctions) >= mis:
            ftemp.append(cg)
            fprune.append(cg)
            F_set_withFrequency.append([cg,count])
        count = 0
    
    # Removing Cannot be together items
    i=0
    #fprune = ftemp
    while i < len(fprune):
        for eachset in cannot_be_together:
            if(set(eachset) <= set(fprune[i])):
                fprune.pop(i)
                F_set_withFrequency.pop(i)
                i = i - 1
                break
        i = i + 1
  
####################################### Generating Tail Count #####################################################
    count = 0
    F_set_tailCount = []
    for temp1 in F_set_withFrequency:
        temp2 = temp1[0][1:]
        tailCount = []
        for transaction in transctions:
            if set(temp2) <= set(transaction):
                count = count + 1
        tailCount.append(temp1)
        tailCount.append(count)
        F_set_tailCount.append(tailCount)
        count = 0
    print("Frequent set with tail count")
    print(F_set_tailCount)
    print("Generated Frequency Set --- F" + str(k))
    if(len(F_set_tailCount) > 0):
        F_set.append(F_set_tailCount)
    j = 0
    for i in range(len(F_set)):
        if i == 0:
            pass
        else:
            if nomust != 1:
                while j < len(F_set[i]):
                    counter = 0
                    for subset in must_have:
                        if str(subset) in F_set[i][j][0][0]:
                            counter = 1
                            break
                    if counter == 0:
                        F_set[i].pop(j)
                        j = j - 1
                    j = j + 1
    print(F_set)
    k = k + 1

####################################### Generating Output File ####################################################	
outputfile = open(r'output-patterns.txt','w+')

for i in range (len(F_set)):
    outputfile.write('Frequent '+str(i + 1)+'-itemsets\n')
    outputfile.write('\n')
    if i == 0:
        j = 0
        while j < len(F_set[i]):
            outputfile.write('\t'+str(F_set[i][j][1])+' : {'+str(F_set[i][j][0])+'}\n')
            j = j + 1
    else:
        j = 0
        while j < len(F_set[i]):
            outputfile.write('\t'+str(F_set[i][j][0][1])+' : {'+str(F_set[i][j][0][0]).replace("[","").replace("]","").replace("'","")+'}\n')
            outputfile.write('Tail count ='+str(F_set[i][j][1])+'\n')
            j = j + 1
    outputfile.write('\n\tTotal number of frequent '+str(i + 1)+'-itemsets = '+str(len(F_set[i]))+'\n\n')
    
outputfile.close()


####################################### End of File ###############################################################





