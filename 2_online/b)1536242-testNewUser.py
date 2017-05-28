#1536242 - Paolo Tamagnini

import time
import pandas as pd
import numpy as np
import csv

#CREATE DF FROM TSV OF 100K RATINGS
data = pd.read_csv('../u.data', 
                   delimiter='\t',
                   names = ['user_id', 'item_id','rating', 'timestamp'])
n = len(data)

#CREATING LIST OF DIFFERENT USER AND LIST OF DIFFERENT FILMS
#WE FIND OUT EACH LIST ARE GROWING NUMBERS FROM 1 TO THE SIZE OF THE LIST
users = data["user_id"]
items = data["item_id"]
users = sorted(set(users))
nU = len(users)
items = sorted(set(items))
nI = len(items)

#CREATE DF FROM u.item THAT DESCRIBES ALL THE nI MOVIES
dataFilm = pd.read_csv('../u.item', 
                   delimiter='|',
                   names = ['movie id',
                             'movie title',
                             'release date',
                             'video release date',
                             'IMDb URL',
                             'unknown',
                             'Action',
                             'Adventure',
                             'Animation',
                             "Children's",
                             'Comedy',
                             'Crime',
                             'Documentary',
                             'Drama',
                             'Fantasy',
                             'Film-Noir',
                             'Horror',
                             'Musical',
                             'Mystery',
                             'Romance',
                             'Sci-Fi',
                             'Thriller',
                             'War',
                             'Western'])




#CREATING LIST OF MOVIE TITLES	
movies = dataFilm['movie title']
#CREATING DICTIONARY CONNECTING movies WITH items
dizMovies=dict(zip(movies,items))

#CREATING MATRIX JUST LIKE THE ONES IN offline.py
#THIS TIME ON THE ENTIRE 100K DATASET THOU

Mdata = np.zeros((nU,nI))
for r in range(0,n):
    i = data["user_id"][r]-1
    j = data["item_id"][r]-1
    Mdata[i,j] = data["rating"][r]
	

#THIS IS LONG BUT EASY,
#I DIVIDED THE GENRES OF MOVIES IN 5 KINDS:
#Easy, Sweet, Complex, Soft and Other
#EACH MOVIE CAN HAVE DIFFERENT GENRES AT THE SAME TIME
#SO INSTEAD OF BOTHERING ABOUT THEIR COMBINATIONS, 
#I DECIDED A KIND OF GENRE OF EACH GENRE.
#GIVEN A MOVIE WITH MANY GENRE OF DIFFERENT KINDS,
#I COUNT THE NUMBER OF PRESENT GENRE OF EACH KIND
#AND I GIVE A KIND TO THE MOVIE

#ALL OF THIS IS WRITTEN IN A DICTIONARY THAT FOR EACH MOVIES GIVES A KIND OF GENRE

dizKinds = {}
listOfKinds = ["Easy","Sweet",'Soft','Other',"Complex"]
dizKinds = dict(zip(range(0,5),listOfKinds))
dizGenre = {}
for i in range(0,nI):
    
    countingKinds = []

    kB = 0
    kG = 0
    kK = 0
    kO = 0
    kW = 0

    if dataFilm['unknown'][i] == 1:
        kO += 1
    if dataFilm['Action'][i] == 1:
        kB += 1
    if dataFilm['Adventure'][i] == 1:
        kB += 1
    if dataFilm['Animation'][i] == 1:
        kK += 1
    if dataFilm["Children's"][i] == 1:
        kK += 1
    if dataFilm["Comedy"][i] == 1:
        kG += 1
    if dataFilm["Crime"][i] == 1:
        kW += 1
    if dataFilm["Documentary"][i] == 1:
        kO += 1
    if dataFilm["Fantasy"][i] == 1:
        kB += 1
    if dataFilm["Film-Noir"][i] == 1:
        kW += 1
    if dataFilm["Horror"][i] == 1:
        kW += 1
    if dataFilm["Musical"][i] == 1:
        kG += 1
    if dataFilm["Mystery"][i] == 1:
        kW += 1
    if dataFilm["Romance"][i] == 1:
        kG += 1
    if dataFilm["Sci-Fi"][i] == 1:
        kB += 1
    if dataFilm["War"][i] == 1:
        kB += 1
    if dataFilm["Western"][i] == 1:
        kW += 1
    if dataFilm["Thriller"][i] == 1:
        kW += 1

    countingKinds.append(kB)
    countingKinds.append(kG)
    countingKinds.append(kK)
    countingKinds.append(kO)
    countingKinds.append(kW)

    indexKind = countingKinds.index(max(countingKinds))
    winningKind = dizKinds[indexKind]

    dizGenre[i] = winningKind

    if i not in dizGenre.keys():
        dizGenre[i] = 'Other'
    if dataFilm["Crime"][i] == 1:
        dizGenre[i] = "Complex"   
    if dataFilm["Musical"][i] == 1:
        dizGenre[i] = "Sweet"
    if dataFilm["Sci-Fi"][i] == 1:
        dizGenre[i] = "Easy"
    if dataFilm["Documentary"][i] == 1:
        dizGenre[i] = 'Other'
    if dataFilm["Horror"][i] == 1:
        dizGenre[i] = "Complex"
    if dataFilm["Animation"][i] == 1:
        dizGenre[i] = "Soft"
    if dataFilm["Children's"][i] == 1:
        dizGenre[i] = "Soft"

		
#LOADING NEW USER FROM CSV FILE

dfNewUserFromCsv = pd.read_csv('newUser.csv', delimiter=',')


#NOW GIVEN THE RATING OF THE NEW USER,
#I CHECK HOW MANY RATINGS ABOVE	R BELONGS TO EACH KIND OF GENRE
#THE KIND OF GENRE THAT GETS MOST OF THE RATINGS ABOVE R
#GIVES THE STATS OF MY NEW USER: 
#listOfKindsPercent WILL CONTAIN THE % OF RATE ABOVE R FOR EACH KIND

R = 4

NewUserRow = np.zeros(nI)
kB = 0
kG = 0
kK = 0
kW = 0
kO = 0

for i in range(0,len(dfNewUserFromCsv)):
    x = dfNewUserFromCsv['item_id'][i]
    y = dfNewUserFromCsv['rating'][i]
    NewUserRow[x-1] = y
    if dizGenre[x-1] == "Easy" and y >= R:
        kB +=1
    if dizGenre[x-1] == "Sweet" and y >= R:
        kG +=1
    if dizGenre[x-1] == "Complex" and y >= R:
        kW +=1
    if dizGenre[x-1] == 'Soft' and y >= R:
        kK +=1
    if dizGenre[x-1] == 'Other' and y >= R:
        kO +=1
listOfKinds = []
listOfKinds.append(kB)
listOfKinds.append(kG)
listOfKinds.append(kK)
listOfKinds.append(kO)
listOfKinds.append(kW)

listOfKindsPercent = np.array(listOfKinds) / float(sum(listOfKinds))
print ' '
print 'The new user stats are:'
print ' '
for i in range(0,len(listOfKindsPercent)):
	print dizKinds[i], '-->', listOfKindsPercent[i]*100,'%'

#CALCULATING DISTANCES FOR NEW USER

DistNewUser = np.zeros(nU)
urif = NewUserRow
for j in range(0,nU):
    count = 0
    listNum = []
    ucomp = Mdata[j,:]
    for item in range(0,nI):    
        if ucomp[item] != 0 and urif[item] != 0 :          
            count += 1        
            a = np.abs(ucomp[item] - urif[item])           
            listNum.append(a)
    
    if not listNum:      
        dj = 5.0
    else:
        dj = sum(listNum)/float(count)
		
    DistNewUser[j] = dj
	
	
#DEFINING ALWAYS FUNCTION TO FIND K NEIGHBOURS

def returnKnearest(k,A):
    Knearest = []
    vett = list(A)
    for i in range(0,k):
        j = vett.index(min(vett))
        Knearest.append(j)
        vett[j] = 100.0
    return Knearest

	
#PREDICTING FROM K NEIGHBOURS THE RATINGS FOR EACH MOVIE OUR USER DIDN'T RATE
#HYPOTHETICALLY IF IT DIDN'T RATE THEM, IT DIDN'T WATCH THEM

k = 150
NewUserRowPredict = np.zeros(nI)
listOfNearest = returnKnearest(k,DistNewUser)
listOfFilmToPredict = []
for j in range(0,nI):
    if NewUserRow[j] == 0.0:
        listOfFilmToPredict.append(j)
        columnKJ = Mdata[listOfNearest,j]
        notNullComp = float(len(np.nonzero(columnKJ)[0]))
        if notNullComp != 0:
            somma =  sum(columnKJ)
            NewUserRowPredict[j] =somma/notNullComp

#SELECTION OF THE RECOMMENDATION			

			
#FOR EACH PREDICTION WE WANT TO KNOW HOW MANY NEIGHBOURS ACTUALLY RATE THE MOVIE.
#THE IDEA IS THAT IF 1 MOVIE HAS BEEN RATED BUT ONLY ONE NEIGHBOUR AND ANOTHER ONE BY ALL OF THEM
#BUT BOTH HAVE A 5 STAR PREDICTION, WE MIGHT BE INTERESTED IN THE SECOND ONE WHO GOT 5
#BECAUSE LOTS OF NEIGHBOURS GAVE A 5 NOT JUST ONE GUY

#selecting neighbours rows from full matrix
M1 = Mdata[listOfNearest,:]

#selecting movies we are predcting
M2 = M1[:,listOfFilmToPredict]

#creating dictionary that given movie gives number of neighbours who rated it
dizHowManyHaveSeenIt = {}

#for each movie to predict..
for j in range(0,len(listOfFilmToPredict)):
    c = 0
	#and for each neighbour..
    for i in range(0,k):

		#let's see if the neighbour watched it..
        if M2[i,j]!=0:
			#if he did,
			#let's count him
            c += 1
	#writing number of neighbour who watched movie j in dictionary
    dizHowManyHaveSeenIt[listOfFilmToPredict[j]]=c
	
	
#NOW WE WANT TO SELECT FROM OUR PREDICTION THE ONES WE ACTUALLY CARE: GOOD PREDICTIONS
#EVERY PREDICTION HIGHER THAN 4 WILL BE SAVED IN THE LIST goodList

listofPred = list(NewUserRowPredict)
goodList = []
for i in range(0,len(listofPred)):
    if listofPred[i] >= 4.0:
        goodList.append(i)
		
		
#IN GOODLIST WE STILL HAVE TOO MANY MOVIES TO RECOMMEND:
#WE NEED TO SELECT THEM BY CHECKING THE MOST POPULAR THANKS TO dizHowManyHaveSeenIt


#IT'S BETTER TO ASK HOW MANY MOVIES THE NEW USER WANTS TO HAVE RECOMMENDED:
nr = 5
while True:
	try:
		print ' '
		nr = int(raw_input('Please, insert the number of movies you want to have recommended:'))
		break
	except (TypeError, ValueError):
		print ' '
		print 'Please write a proper number!'

#IF THEY ASK TOO MANY WE'LL TELL THEM
if nr > len(goodList):
	print ' '
	print 'We are sorry, you ask too many!' 
	print 'We will print out the maximum we have for you:',len(goodList)
	nr = len(goodList)

#CREATING DICTIONARIES, ONE FOR EACH KIND, THAT WILL TELL HOW MANY HAVE SEEN A MOVIE
#THE KEYS OF dizViewsOfGoodListB FOR EXAMPLE WILL LIST ALL THE MOVIES OF "Easy" IN goodList
#THE VALUES WILL TELL THE VIEWS FO EACH OF THEM
dizViewsOfGoodListB = {}
dizViewsOfGoodListG = {}
dizViewsOfGoodListW = {}
dizViewsOfGoodListK = {}
dizViewsOfGoodListO = {}
kB = 0
kG = 0
kK = 0
kW = 0
kO = 0
for x in goodList:
	
	if dizGenre[x] == "Easy":
		dizViewsOfGoodListB[x] = dizHowManyHaveSeenIt[x]
		kB +=1
	if dizGenre[x] == "Sweet":
		dizViewsOfGoodListG[x] = dizHowManyHaveSeenIt[x]
		kG +=1
	if dizGenre[x] == "Complex":
		dizViewsOfGoodListW[x] = dizHowManyHaveSeenIt[x]
		kW +=1
	if dizGenre[x] == 'Soft':
		dizViewsOfGoodListK[x] = dizHowManyHaveSeenIt[x]
		kK +=1
	if dizGenre[x] == 'Other':
		dizViewsOfGoodListO[x] = dizHowManyHaveSeenIt[x]
		kO +=1 

#WE MAKE A LIST THAT TELLS THE AMOUNT OF EACH KIND IN goodList	
listOfAmountKindsGoodList = []
listOfAmountKindsGoodList.append(kB)
listOfAmountKindsGoodList.append(kG)
listOfAmountKindsGoodList.append(kK)
listOfAmountKindsGoodList.append(kO)
listOfAmountKindsGoodList.append(kW)

#WE MAKE A LIST OF DICTIONARIES, ONE FOR EACH KIND
listOfDictViewsPerKindGoodList = []
listOfDictViewsPerKindGoodList.append(dizViewsOfGoodListB)
listOfDictViewsPerKindGoodList.append(dizViewsOfGoodListG)
listOfDictViewsPerKindGoodList.append(dizViewsOfGoodListK)
listOfDictViewsPerKindGoodList.append(dizViewsOfGoodListO)
listOfDictViewsPerKindGoodList.append(dizViewsOfGoodListW)

numRec = 0

#GIVEN listOfKindsPercent WITH THE STATS OF THE NEW USER
#WE WANT TO CREATE A LIST listOfRecomPerKind THAT GIVES THE NUMBER OF MOVIES OF EACH KIND 
#WE WANT TO RECOMEND. THIS WILL BE CALCULATED THANKS TO TAKING THE LOWER INTEGER OF KIND%*nr
listOfRecomPerKind = np.zeros(len(listOfKindsPercent))

for p in range(0,len(listOfKindsPercent)):
	listOfRecomPerKind[p]=np.floor(listOfKindsPercent[p]*nr)

#IF BY APPROXIMATING TO INTEGERS WE DON'T MAKE IT TO nr RECOMMENDED MOVIES,
#WE REACH nr BY ADDING MORE MOVIES TO THE KIND WITH LARGERST SHARE
if sum(listOfRecomPerKind) < nr:
	listForNow = list(listOfRecomPerKind)
	maxInd = listForNow.index(max(listForNow))
	listOfRecomPerKind[maxInd] = listOfRecomPerKind[maxInd] + nr - sum(listOfRecomPerKind)

#IF THEN THERE AREN'T ENOUGH MOVIE OF A KIND IN goodList TO SATISFY OUR USER STATS,
#(MAYBE BECAUSE THE CHOSEN nr IS TOO BIG) THEN WE MUST SET THE AMOUNT OF RECOMMENDED MOVIES
#OF THAT KIND TO THE BEST WE CAN DO
for p in range(0,len(listOfKindsPercent)):
	if listOfRecomPerKind[p] > listOfAmountKindsGoodList[p]:
		listOfRecomPerKind[p] = listOfAmountKindsGoodList[p]
		
#WE MAKE SURE nr IS IN THE END EQUAL TO THE SUM OF RECOMMENDED MOVIES PER KIND
nr = sum(listOfRecomPerKind)

#FINALLY WE CAN PICK FROM goodList THE RECOMMENDED MOVIES UNTIL WE HAVE nr OF THEM
#AND WE DO THAT BY PICKING ONE KIND AT A TIME
#MAKING SURE WE GET ENOUGH FOR EACH MOVIES IN THE SAME PROPORTION OF THE USER STATS

listOfReccInGoodList = []	

while numRec < nr:
	for p in range(0,len(listOfKindsPercent)):
		nk = 0
		while nk < listOfRecomPerKind[p]:
			keyMax = max(listOfDictViewsPerKindGoodList[p], key=listOfDictViewsPerKindGoodList[p].get)
			#print dataFilm['movie title'][keyMax],'-->', dizGenre[keyMax],nk
			listOfReccInGoodList.append(keyMax)
			nk += 1
			numRec += 1
			
			listOfDictViewsPerKindGoodList[p][keyMax] = 0.0

#NOW WE CAN PRINT OUT OUR RECOMMENDATION!!
#AND OUTPUT A TXT OF TITLES!!
f = open('recommendedMovies.txt','w')
scriba = csv.writer(f)
for x in listOfReccInGoodList:
	print ' '
	print dataFilm['movie title'][x]
	scriba.writerow([dataFilm['movie title'][x]])
	
