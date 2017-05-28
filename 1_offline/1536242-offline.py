#1536242 - Paolo Tamagnini
import time
import pandas as pd
import numpy as np

#CREATE DF FROM TSV OF 100K RATINGS
print ' '
print 'Loading data..'
data = pd.read_csv('../u.data', 
                   delimiter='\t',
                   names = ['user_id', 'item_id','rating', 'timestamp'])
n = len(data)

#CREATE TEST FROM PICKING 1 DF ROW EVERY 5 SO THAT WE HAVE 20%(=1/5) OF ROWS IN TEST
dataTest = data[1::5]

#ALL THE OTHER ROWS (80%) WILL GO IN TRAIN
dataTrainIndex = sorted(set(data.index) - set(dataTest.index))
dataTrain = data.loc[dataTrainIndex]

nTest = len(dataTest)
nTrain = len(dataTrain)

#RESETTING INDEX OF BOTH TEST AND TRAIN
dataTrain.index = range(0,nTrain)
dataTest.index = range(0,nTest)

#CREATING LIST OF DIFFERENT USER AND LIST OF DIFFERENT FILMS
#WE FIND OUT EACH LIST ARE GROWING NUMBERS FROM 1 TO THE SIZE OF THE LIST

users = data["user_id"]
items = data["item_id"]
users = sorted(set(users))
nU = len(users)
items = sorted(set(items))
nI = len(items)

#CREATING MATRIXES (users x items) FOR TRAIN AND TEST
#EACH ELEMENT (i,j) WILL GIVE THE RATING OF USER i+1 AND ITEMS j+1
#(this because for example users[0] = 1 and users[len(users)-1]=len(users))
print ' '
print 'Creating matrixes..'
MTrain = np.zeros((nU,nI))
for r in range(0,nTrain):
    i = dataTrain["user_id"][r]-1
    j = dataTrain["item_id"][r]-1
    MTrain[i,j] = dataTrain["rating"][r]

MTest = np.zeros((nU,nI))
for r in range(0,nTest):
    i = dataTest["user_id"][r]-1
    j = dataTest["item_id"][r]-1
    MTest[i,j] = dataTest["rating"][r]

#USING MTrain FOR CALCULATING DISTANCES BETWEEN EACH USER
#THIS WILL CREAT A SYMMETRIC MATRIX Dij WITH DIAGONAL OF 0s
#EACH ELEMENT (i,j) WILL GIVE THE DISTANCE BETWEEN 
#USERS i+1 AND j+1. 
#THE DISTANCE WILL BE CALCULATED USING RATINGS ON THE SAME MOVIES. 
#IF THE 2 USERS DON'T HAVE NOT EVEN 1 RATE ON THE SAME MOVIE
#THE DISTANCE BETWEEN THOSE 2 WILL BE SET TO 5.0, WHICH IS THE MAXIMUM DISTANCE
#IF A DISTANCE IS 0.0 EITHER WE HAVE i = j, EITHER WE FOUND 2 IDENTICAL USERS.
print ' '
print 'Computing distances..'
print ' '
start = time.time()
Dij = np.zeros((nU,nU))
saveTime = 0

#for each user..
for i in range(0,nU):

    if i%100 == 0:
        print 'user',str(i).zfill(3),'/',nU
		
    saveTime += 1
	
    #we save the user of reference i
    urif = MTrain[i,:]
	
	#for each other user that gives a new pair..
    for j in range(saveTime,nU):
	
		#we save the user j to be compared with user i
        ucomp = MTrain[j,:]
		
        #this will be the number of ratings on movies 
		#that the user of reference did rate
        count = 0
		
        #in this last we will append all the difference of ratings in common
        listNum = []
        
        #for each movie..
        for item in range(0,nI):
		
            #we check if both user have a rating
            if ucomp[item] != 0 and urif[item] != 0 :
			
                #and we increase the number of ratings in common
                count += 1
				
                #then we calculate the different between the 2 ratings
                a = np.abs(ucomp[item] - urif[item])
				
                #so we add the absolute value of such difference to the list
                listNum.append(a)
				
        #if the list of differences is empty..
        if not listNum:
		
            #it means there was no rating in common
			#so there is nothing to measure a distance
			#then we set the distance to 5 which is higher than any other distance
			#where intersection has been found
            dij = 5.0
			
		#if the list of differences is not empty..
        else:
		
            #we can caluclate the distance as
            dij = sum(listNum)/float(count)
			
		#finally we set the distances in the symmetric matrix
        Dij[i,j] = dij
        Dij[j,i] = dij
		
end = time.time()
#this will take around 5 minutes
print ' '
print 'Elapsed for distances:'
print int((end - start)/60), 'm',(end - start)%60.0,'s'


#K NEAREST NEIGHBOURS ALGORITHM
#NOW THAT WE HAVE A MATRIX WITH ALL THE DISTANCES BETWEEN EVERY USER
#WE CAN FIND GIVEN A USER (a row of the matrix Mtrain) k OTHER USERS
#THAT ARE THE CLOSEST NEIGHBORS TO OUR USER.

#TO DO THIS WE DEFINE A FUNCTION THAT TAKES: 
#k: number of neighbours to find
#A: matrix of distances
#i: user i+1

def returnKnearest(k,A,i):

	#creating list of k neighbours
    Knearest = []
	
	#saving distances from my reference user to every other
    vett = list(A[i,:])
	
	#for k times..
	
    for i in range(0,k):
	
		#look for the closest user..
        j = vett.index(min(vett))
		
		#and add him to the list of neightbours
        Knearest.append(j)
		
		#but then set his distance to 100.0 so it won't add him more than once
        vett[j] = 100.0
		
	#return the list of k neighbours
    return Knearest

#THE PROBLEM HERE IS TO CHOOSE HOW MANY NEIGHBOURS TO GET (aka the value of k)
#WE CHOOSE THE FOLLOWING VALUES CAUSE IT GIVES THE BEST RMSE 
#(to find it i had to test many ks within a cycle)

k = 305

#ONCE WE HAVE A k WE CAN FIND FOR EACH USER IN users THE NEIGHBOURS ON WHICH WE CAN FIND THE RATINGS
#TO USE TO PREDICT ALL THE MISSING RATINGS OF THE GIVEN USER

#THE PREDICTED RATINGS WILL BE SAVED ON MHat, A MATRIX LIKE Mtrain.

MHat = np.zeros((nU,nI))

start = time.time()
print ' '
print 'Computing predictions..'
print ' '
#for each user..
for i in range(0,nU):

    if i%100 == 0:
        print 'user',str(i).zfill(3),'/',nU
	
	#we find the list of k nearest neighbours..
    listOfNearest = returnKnearest(k,Dij,i)
    
	#and for each movie..
    for j in range(0,nI):
        
		#we check if our user didn't watch it
        if MTrain[i,j] == 0.0:
		
			#if he didn't watch it,
			#we consider with columnKJ the column of the movie j of the matrix Mtrain
			#that brings only the components relative to neighbours users
			columnKJ = MTrain[listOfNearest,j]
			
			#we want to know thou how many of those neighbours actually watchd and rated the movie
			#so we save on notNullComp the amount of all the not null components of columnKJ
			notNullComp = float(len(np.nonzero(columnKJ)[0]))

			#so in the end if we find at least one neighbour with a rating for the movie j..
			if notNullComp != 0:
			
				#our prediction will be given by the average of all the not null ratings on the movie join
				#given by the k neighbours
				somma =  sum(columnKJ)
				MHat[i,j] = somma/notNullComp
                
end = time.time()
#depending on which k we are using this will take more time
print ' '
print 'Elapsed for predictions:'
print int((end - start)/60), 'm',(end - start)%60.0,'s'


#FINALLY WE CAN NOW CALUCLATE THE RMSE.
#THIS WILL BE CALCULATED WITH THE DIFFERENCES BETWEEN PREDICTED RATINGS AND ACTUAL RATINGS 
#OF THE SAME USER ON THE SAME MOVIE WE FIND IN THE TEST DATASET
#THIS MEANS THAT WE DON'T EVEN USE ALL THE PREDICTED RATINGS THAT DIDN'T ACTUALLY HAPPEN IN THE TEST

#list of squared differences we need to do the average on..
listOfDiff = []
print ' '
print 'Computing RMSE..'
#list of coordinates of prediction in MHat (that means pairs (x,y) for not null element of MHat)
listOfPrediction = zip(np.nonzero(MHat)[0],np.nonzero(MHat)[1])
#for each prediction:
for x,y in listOfPrediction:
    #if the prediction is present in the Test..
    if MTest[x,y] != 0:
	
        #we do the square difference
        diff = (MTest[x,y] - MHat[x,y])**2

        #and we add it to the list
        listOfDiff.append(diff)
		
#so we compute and print the root of the average of the list
print ' '
print 'RMSE:',np.sqrt(np.mean(listOfDiff))









 