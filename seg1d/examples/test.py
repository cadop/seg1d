'''A method for a user to run the doctests without building documentation
Suggested use:

from seg1d.examples import test
test.run()
'''

print('Imported Testing Setup')
print('Use: test.run() to start tests')

from . import *
import seg1d

def run():
    import doctest
    
    print("\nTesting GAUSS Example")
    print(doctest.testmod(ex_gauss))
    
    print("\nTesting SIMPLE Example")
    print(doctest.testmod(ex_simple))
    
    print("\nTesting ECG Example")
    print(doctest.testmod(ex_ecg))
    
    print("\nTesting SINE Example")
    print(doctest.testmod(ex_sine))
    
    print("\nTesting SINE NOISE Example")
    print(doctest.testmod(ex_sin_noise))

    print("\nTesting SEGMENTER FEATURES Example")
    print(doctest.testmod(ex_segmenter_features))

    print("\nTesting SEGMENTER SINE Example")
    print(doctest.testmod(ex_segmenter_sine))

    print("\nTesting Segmenter Class")
    print(doctest.testmod(seg1d.segment))
    
    print("\nTesting Algorithm Methods")
    print(doctest.testmod(seg1d.algorithm))

    print("Finished running tests \n")

if __name__ == '__main__':
    run()