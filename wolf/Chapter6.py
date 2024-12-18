'''
We got the very best our model could spit out.
Now, as promised, we'll use R squared to compare our model to the data.
Then our guess of 2/x to the model. And then the guess to the data.
We agree that R > 0.95 constitues a good enough math for our purposes

SIDENOTE: You might have noticed that the guess suddenly changed from 1/x
to 2/x. This is because I genuinely believed the answer to be 1/x, then the
model started sorta gravitating toward 2/x, but not quite close. Soon I realized
that 2/x is probably the answer and the model is being a bit overfitted.
Guess it's a case of a feedback loop between me and the model.

'''
import numpy as np

import json #JASOOON

def Rsq(Y, Yhat):
    y = np.mean(Y)
    SSres = np.sum((Y - Yhat)**2)
    SStot = np.sum( (Y - y)**2 )

    res = 1 - SSres/SStot
    return res


BEST = open( 'BEST.json', 'r' )
data = json.load( BEST )

loss = data[0]
params = data[1]


DATA = open( 'DB.json', 'r' )
data = json.load( DATA )
#data again made sparser due to overfitting
X = np.array( data['X'] ).astype( float )[0::5]
Y = np.array( data['Y'] ).astype( float )[0::5]

Ymodel = params['a'] * 1/X + params['c']
Yguess = 2/X

print( f'R^2 DATA,  MODEL: { Rsq( Y, Ymodel ) }' )
print( f'R^2 MODEL, GUESS: { Rsq( Ymodel, Yguess )} ')
print( f'R^2 DATA,  GUESS: { Rsq( Y, Yguess ) }')

'''

If You dared to run the script before changing any of the previous files,
You could see the values 
0.995
0.993
0.988

Which means that everything fits together nicely and 2/n is a pretty
good approximation to the problem posed in Chapter1, given variability
of the generated data.

There's no champagne. No fireworks. No nothing.
We did a regression model that works on very specific cases,
with a lot of tweaking neccesary.
But, while it is but a small brick, it shall pave the way to solutions
of much grander problems.
Hopefully.

'''