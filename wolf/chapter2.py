'''
Step (2) is pretty straightforward
For N < MAX_N run CASES_NUM cases, count the number of positive ones, then write the probability
positives/CASES_NUM in a dictionary for N
The dictionary is then saved to a json (press X to Jason kekekek), in order to be used further down the line

If for some reason You don't have nothing better to do: maybe Your date got cancelled,
maybe Your favourite program is delayed (that even possible?), maybe You're avoiding visiting Your mother
by saying You got " work " to do (if that's the case, call the poor woman).
Whatever the case may be, I highly encourage you to tweak the values below, run the script, and see how
my programs absolutely crumble under the weight of a miniscule amount of unpredictability.

Though i encourage You to do that, I also highly suggest doing it after firstly checking out the rest of the story,
to see what the world would look like if there was no evil nor ill intent in it.

By the way, be wary. As MAX_N gets larger the generation takes longer (duh). MAX_N = 1000 with CASES_NUM  = 100 is feasible. 
MAX_N < 200 with CASES_NUM = 1000 isn't bad, but it's not good either. Beyond that, who knows what happens? 
If the amount of Your free time coincides with the lifetime of the universe - be my guest and cross this barrier.

'''
CASES_NUM = 1000
MAX_N = 100

import random
def gen( n ):

    wolf = 0
    opposite = n//2

    eaten = [False for i in range( n )]
    eaten[wolf] = True

    eaten_num = 1

    while True:
        #roll for a move
        if random.randint(0, 1) == 0:
            wolf -= 1
        else:
            wolf += 1

        #check boundry conditions
        if wolf == -1:
            wolf = n-1
        elif wolf == n:
            wolf = 0

        if not eaten[wolf]:
            eaten_num += 1
            eaten[wolf] = True

        #check termination condition
        if wolf == opposite:
            if eaten_num == n:
                return True
            else:
                return False
            
CASES_NUM = 10000
MAX_N = 100

#calculate times

dataX = []
dataY = []
for n in range( 2, MAX_N + 2, 2 ):
    positive = 0
    print(n)
    for i in range( CASES_NUM ):
        if gen( n ):
            positive += 1
    dataX.append( n )
    dataY.append( positive/CASES_NUM )


#print(res)
import json
res = {
    'X' : dataX,
    'Y' : dataY
}
DB = open( 'DB.json', 'w' )
DB.write( json.dumps( res ) )

#save to json

# import time

# t0 = time.time()
# print( f'dt {time.time() - t0}' )

# def measure_time( n, cases_num ):
#     t0 = time.time()
#     probability( n, cases_num )
#     print( f'N: {n} dt: {time.time() - t0}' )