'''
A very rudimentary implementation of ID3 algorithm (i think) for building decision trees.

Data was borrowed from here:
https://www.kaggle.com/datasets/pablomgomez21/drugs-a-b-c-x-y-for-decision-trees

To be completely honest, I don't know if I can use this data as part of the portfolio, but here we are.
Then again, I don't see any Data Science Police around, do you? You better not...

Anyway, build.py has the algorithm itself which is pretty standard.
This file uses 5-fold cross validation to estimate average success rate of the algorithm on the data.
It turns out to be ~0.85, which... well.. could be better

I conservatively consulted 'AI: A Mordern Approach' by Russel, Norvig, Section 18.3: Learning Decision Tree (duh)
while working on it.

(FLEX) While reading the abovementioned chapter I paused at the first mention of 'attributes' in order
to predict what the algorithm's gonna be. In the next 3 migraine-induced hours I did in fact independently
come up with an idea that if the tree is gonna split on the best attribute, I'd better have a good mathematical idea
of what 'best' means. This naturally lead me to the chapter on entropy in Blitzstein, Hwang. Long story short
I NEARLY got the formulas for entropy gain correct.

Why am I telling You thay? Dunno. Just proud I guess.

'''
import pandas as pd
import numpy as np

from builder import builder

def row_to_dict(row):
    res = {}
    for key, val in row[1].items():
        res[key] = val
    return res

# # # # # # # # # # # # # # # # # 


K = 5

df = pd.read_csv( 'drug.csv' )
frags = np.array_split( df, K )



target = 'Drug'
attributes = df.columns.drop(target)

success_rates = []

for i in range( K ):
    train_data = pd.concat( [frags[j] for j in range(K) if j != i], ignore_index=True )
    test_data = frags[i]
    
    root = builder( train_data, attributes, target )

    positive = 0
    total    = test_data.shape[0]

    for row in test_data.iterrows():
        #row to dict
        test_case = row_to_dict( row )
        prediction = root.klassify( test_case )
        if test_case[target] == prediction:
            positive += 1

    success_rates.append( positive/total ) 
    print( f'SET {i}\nSUCCESS RATE: {success_rates[i]}\n' )



print( f'AVERAGE SUCCESS RATE: {sum( success_rates ) / len(success_rates )}' )
        # root.klassify( row )







