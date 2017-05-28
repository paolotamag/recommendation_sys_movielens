#1536242 - Paolo Tamagnini

import time
import pandas as pd
import numpy as np

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
dizMovies=dict(zip(movies,range(1,1683)))

#BY RUNNING THIS FILE YOU ARE ABLE TO CREATE A NEW USER: YOURSELF
print ' '
print 'Please, give a rating for each movie!'
print ' '
print 'The rating must be between 0 and 5.'
print ' '
print "Please write 0 only if you haven't seen the movie."
print ' '

time.sleep(1)
print 'Movie rating survey starting now..'
print ' '
print '-----------'
time.sleep(1)


listTitles = []

x = 'Star Wars (1977)'
listTitles.append(x)
x = 'Independence Day (ID4) (1996)'
listTitles.append(x)
x = 'Jurassic Park (1993)'
listTitles.append(x)
x = 'Indiana Jones and the Last Crusade (1989)'
listTitles.append(x)

x = "Breakfast at Tiffany's (1961)"
listTitles.append(x)
x = 'Ghost (1990)'
listTitles.append(x)
x = 'Grease (1978)'
listTitles.append(x)
x = 'Pretty Woman (1990)'
listTitles.append(x)

x = 'Toy Story (1995)'
listTitles.append(x)
x = 'Lion King, The (1994)'
listTitles.append(x)
x = 'Snow White and the Seven Dwarfs (1937)'
listTitles.append(x)
x = 'Home Alone (1990)'
listTitles.append(x)

x = 'Shining, The (1980)'
listTitles.append(x)
x = 'Fargo (1996)'
listTitles.append(x)
x = 'Silence of the Lambs, The (1991)'
listTitles.append(x)
x = 'Pulp Fiction (1994)'
listTitles.append(x)

from random import shuffle
shuffle(listTitles)


listMovies = []
listRatings = []

for x in listTitles:
	listMovies.append(dizMovies[x])
	print ' '
	print x
	
	r = 6
	while r not in range(0,6):
		try:
			print ' '
			r = int(raw_input('please type a number for your rating:'))
			if r not in range(0,6):
				print ' '
				print 'Please give a value between 0 and 5!'
		except (TypeError, ValueError):
			print ' '
			print 'Please give a value between 0 and 5!'
	listRatings.append(r)
	print ' '
	print '-----------'


dfNewUser = pd.DataFrame()
dfNewUser['item_id'] = listMovies
dfNewUser['rating'] = listRatings

dfNewUser.to_csv('newUser.csv',index = False)


