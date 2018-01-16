
import numpy as np
import random
import re

data=np.array((1,2,3,4))

print data

def demo_random():
   # print random.random()
    data=list()
    print random.choice(range(0,100,3))
    for i in range(0,100000):
       data.append(random.randint(0,123))

    pos=data.index(123)
    print data[pos:pos+5]

def demo_re():
    str='23@qq.com;odosp@gmail.com'
    p=re.compile('([\d]+)@[\w]+.com')
    print p.findall(str);


if __name__=='__main__':
    demo_random()
    demo_re()