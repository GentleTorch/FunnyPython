
import numpy as np
import random

data=np.array((1,2,3,4))

print data

def demo_random():
    print random.random()
    print random.choice(range(0,100,3))

if __name__=='__main__':
    demo_random()