'''
Well well well.
We got pretty everything we want. The last thing to do is the thing that could've been done without a lot
of conversational filler, which is:
(1) get the data
(2) feed it to the model
(3) see what he comes up with

In order to introduce some semblance of scientific rigor, we'll run a couple seperate models and see
which one does best, i.e. which managed to lower the loss function the most.

Then we'll compare the best one with our prediction of 1/x via R squared
If R squared is say > 0.95, we'll consider it good enough for us to say
that that (1/x) fits the data accurately.

In this file the, let's just generate what we gotta generate, save the best result ina file,
and hopefully the next Chapter will get us the precious, precious answers.



EDIT: After extensive testing I encountered a problem. Given the loss function is MSE,
the model tended to go under the graph at the beginning, crooss it, and then go over it.
Then it usually wouldn't budge. While in any other problem this might be fine, 
in this one the value for 2 MUST be 1, and according to the average model it would be ~1.8. 
A big no no.

My guess as to why it wouldn't move is that after loss function
reaches a certain point, the A requires a heavier 'push' than the C parameter, 
and usually a tiny budge to the C parameter is much more impactful with respect to the loss fucntion
than to A (think how much error sliding the model alomng the Y direction can add).
So, C sits in some local minimum and won't let A out.

Then it occured to me: all these reading about overfitting finally paid off! Overfitting is actually the case here (kinda).
My dataset inlucdes 50 points, value for most of them being miniscule - they carry too much weight
compared to value for 2. Hence, taking every fifth input and output pair seemed to do the trick.
Thank God.



SIDENOTE: You might wanna ask: well then, why didn't we just preemptively compare (1/x)
to the data via R squared, and check if it's already > 0.95. To that I say:
I wish I thought of that before writing all the other stuff.
'''

import json # JAASOOOON
import numpy as np
from math import log10

class Model:
    def __init__(self):

        self.params = {
            'a' : 1,#np.random.uniform(-1, 1),
            'b' : 0,
            'c' : 0#np.random.uniform(-1, 1)
        }
        self.derivatives = dict( self.params )

        for val in self.params.values():
            val = np.random.uniform( -10, 10 )

    def loss( self, Y, Yhat ):
        return np.mean( (Y - Yhat)**2 )

    def forward(self, X):

        a = self.params['a']
        b = self.params['b']
        c = self.params['c']

        Yhat = a*((X+b)**(-1)) + c
        return Yhat
        

    def backward(self, X, Y, Yhat):
        a = self.params['a']
        b = self.params['b']
        c = self.params['c']

        df = Y - Yhat

        derivatives = {}
        derivatives['a'] = -2*np.mean( np.multiply( df, (X + b)**(-1) ) )
        #derivatives['b'] = -2*np.mean( np.multiply( df, -a*(X+b)**(-2)) ) 
        derivatives['c'] = -2*np.mean( df )

        return derivatives
    
    def update_params(self, derivatives, lr):


        self.params['a'] = self.params['a'] - lr * derivatives['a']
        #self.params['b'] = self.params['b'] - lr * derivatives['b']
        self.params['c'] = self.params['c'] - lr * derivatives['c']

    def train( self, X, Y, lr, epochs):
        # Yhat = self.forward( X )
        # derivatives = self.backward( X, Y, Yhat )
        # self.update_params( derivatives, lr )



        for i in range( epochs ):

            #lr0 = lr * float(10)**(-log10(i+1))
            Yhat = self.forward( X )
            #lr0 = lr * 1/(10**log10( self.loss(Y, Yhat) ))
            #lr0 = lr
            derivatives = self.backward( X, Y, Yhat )
            self.update_params( derivatives, lr )

        return ( self.loss( Y, self.forward(X) ), self.params )
    
#read data
file = open( 'DB.json', 'r' )
data = json.load( file )

X = np.array(data['X']).astype( float )[0::5]
Y = np.array(data['Y']).astype( float )[0::5]

LR = 0.01
EPOCHS = 10000
MODELS = 100


results = []

for i in range( MODELS ):
    results.append( Model().train( X, Y, LR, EPOCHS ) )

best = min( results, key=lambda res: res[0] )


print( best )
BEST = open( 'BEST.json', 'w' )
BEST.write( json.dumps( best ) )
#save the best

