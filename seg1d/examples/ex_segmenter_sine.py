'''
An example of instancing the Segmenter class to use the convenience methods on array data

.. plot::

    >>> import seg1d
    >>> import numpy as np
    >>> import matplotlib.pylab as plt

    Then we generate some data

    >>> x = np.linspace(-np.pi*2, np.pi*2, 2000) #create an array of data
    >>> targ = np.sin(x)  # target data from a sin function
    >>> t_s,t_e = 200,400 # define a sub-series
    
    To assign the data to the Segmenter, first we create an instance of it and then
    use the ``set_target()`` and ``add_reference()`` methods.

    >>> s = seg1d.Segmenter()  # instance of the segmenter
    >>> s.minW, s.maxW, s.step = 98, 105, 1  # scaling parameters
    >>> s.set_target(targ) # set target and reference data
    >>> s.add_reference(targ[t_s:t_e])
    >>> segments = s.segment() # run segmentation algorithm
    >>> np.around(segments, decimals=7)
    array([[2.000000e+02, 4.000000e+02, 1.000000e+00],
           [1.200000e+03, 1.398000e+03, 9.999999e-01]])
    
    Using matplotlib we can visualize the results

    >>> plt.figure(figsize=(10,3)) #doctest: +SKIP
    >>> #plot the full sine wave
    >>> plt.plot(x, targ,linewidth=8,alpha=0.2,label='Target') #doctest: +SKIP
    >>> #plot the original reference segment
    >>> plt.plot(x[t_s:t_e], targ[t_s:t_e],linewidth=6,alpha=0.7,label='Reference') #doctest: +SKIP
    >>>
    >>> #plot all segments found
    >>> seg_num = 1
    >>> for s,e,c in segments:
    ...     plt.plot(x[s:e], targ[s:e],dashes=[1,1],linewidth=4,alpha=0.8, #doctest: +SKIP
    ...     label='Segment {}'.format(seg_num)) #doctest: +SKIP
    ...     seg_num += 1 #doctest: +SKIP
    >>> plt.xlabel('Angle [rad]') #doctest: +SKIP
    >>> plt.ylabel('sin(x)') #doctest: +SKIP
    >>> plt.legend() #doctest: +SKIP
    >>> plt.tight_layout() #doctest: +SKIP
    >>> plt.show() #doctest: +SKIP

'''


def run():
        
    import seg1d
    import numpy as np
    import matplotlib.pylab as plt

    # create an array of data
    x = np.linspace(-np.pi*2, np.pi*2, 2000)
    # get an array of data from a sin function
    targ = np.sin(x)
    # define a segment within the sine wave to use as reference
    t_s, t_e = 200, 400

    # Make an instance of the segmenter
    s = seg1d.Segmenter()

    # set scaling parameters
    s.minW, s.maxW, s.step = 98, 105, 1
    # Set target and reference data
    s.set_target(targ)
    s.add_reference(targ[t_s:t_e])
    # call the segmentation algorithm
    segments = s.segment()

    print(segments)

    plt.figure(figsize=(10, 3))
    # plot the full sine wave
    plt.plot(x, targ, linewidth=8, alpha=0.2, label='Target')
    # plot the original reference segment
    plt.plot(x[t_s:t_e], targ[t_s:t_e], linewidth=6, alpha=0.7, label='Reference')
    # plot all segments found
    seg_num = 1
    for s, e, c in segments:
        plt.plot(x[s:e], targ[s:e], dashes=[1, 1], linewidth=4, alpha=0.8,
                 label='Segment {}'.format(seg_num))
        seg_num += 1
    plt.xlabel('Angle [rad]')
    plt.ylabel('sin(x)')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run()
