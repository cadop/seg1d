'''
Example using included sample data 

>>> import seg1d 
>>> import numpy as np
>>> #retrieve the sample reference, target, and weight data
>>> r,t,w = seg1d.sampleData()
>>> ### define some test parameters
>>> minW = 70 #minimum percent to scale down reference data
>>> maxW = 150 #maximum percent to scale up reference data
>>> step = 1 #step to use for correlating reference to target data
>>> #call the segmentation algorithm
>>> np.around( seg1d.segment_data(r,t,w,minW,maxW,step) , decimals=7 )
array([[207.       , 240.       ,   0.9124224],
       [342.       , 381.       ,   0.8801901],
       [ 72.       , 112.       ,   0.8776795]])

'''

if __name__ == "__main__":
    
    import seg1d

    #retrieve the sample reference, target, and weight data
    r,t,w = seg1d.sampleData()

    ### define some test parameters
    minW = 70 #minimum percent to scale down reference data
    maxW = 150 #maximum percent to scale up reference data
    step = 1 #step to use for correlating reference to target data

    #call the segmentation algorithm
    segments = seg1d.segment_data(r,t,w,minW,maxW,step)

    print(segments)