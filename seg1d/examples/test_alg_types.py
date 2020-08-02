import pytest
import numpy as np
import seg1d 


class TestRolling:

    x = np.sin( np.linspace(-np.pi*1, np.pi*1, 20) )
    yData = np.sin( np.linspace(-np.pi*2, np.pi*2, 80) ).reshape(4,20)
    winSize = 10

    @pytest.mark.parametrize("x", [[0, 1], {0, 1}, 1, '1', -1, 1.1])
    def test_x_type(self, x):
        """ Check that x type is caught
        """

        with pytest.raises(AssertionError, match=r"must be Numpy Array"):
            seg1d.algorithm.rolling_corr(x, self.yData, self.winSize)

    @pytest.mark.parametrize("yData", [[0, 1], {0, 1}, 1, '1', -1, 1.1])
    def test_yData_type(self, yData):
        """ Check that yData type is caught
        """

        with pytest.raises(AssertionError, match=r"must be Numpy Array"):
            seg1d.algorithm.rolling_corr(self.x, yData, self.winSize)

    @pytest.mark.parametrize("winSize", [np.array([0, 1]), [0, 1], {0, 1}, '1', 1.1])
    def test_winSize_type(self, winSize):
        """ Check that winSize type is caught
        """

        with pytest.raises(AssertionError, match=r"must be an Integer"):
            seg1d.algorithm.rolling_corr(self.x, self.yData, winSize)

    @pytest.mark.parametrize("cMax", [np.array([0, 1]), [0, 1], {0, 1}, '1', 1.1])
    def test_cMax_type(self, cMax):
        """ Check that cMax type is caught
        """

        with pytest.raises(AssertionError, match=r"must be a Boolean"):
            seg1d.algorithm.rolling_corr(self.x, self.yData, self.winSize, cMax)


class TestCombine:
    
    # Default known datatypes

    def s(f1, f2, f3): return np.sin( np.linspace(f1, f2, f3) )
    x = {
        10: {'a': s(-np.pi*0.8, 0, 10), 'b': s(0, np.pi*0.8, 10)},
        20: {'a': s(-np.pi*0.7, 0, 10), 'b': s(0, np.pi*0.7, 10)}
    }
    w = {'a': 0.5, 'b': 0.9}

    @pytest.mark.parametrize("x", [np.array([0, 1]), [0, 1], 1, '1',  1.1])
    def test_x_type(self, x):
        """ Check that x type is caught
        """

        with pytest.raises(AssertionError, match=r"must be a Dict"):
            seg1d.algorithm.combine_corr(x, self.w)
            
    @pytest.mark.parametrize("x", [{"1": [0, 1]}, {(0, 1): [0, 1]}])
    def test_x_key_type(self, x):
        """ Check that the x key type is caught
        """

        with pytest.raises(AssertionError, match=r"must be int"):
            seg1d.algorithm.combine_corr(x, self.w)

    @pytest.mark.parametrize("w", [np.array([0, 1]), [0, 1], 1, '1', 1.1])
    def test_w_type(self, w):
        """ Check that w type is caught
        """

        with pytest.raises(AssertionError, match=r"must be a Dict"):
            seg1d.algorithm.combine_corr(self.x, w)

    @pytest.mark.parametrize("w", [{1: [0, 1]}, {(0, 1): [0, 1]}, {1.1: [0, 1]}])
    def test_w_key_type(self, w):
        """ Check that the w key type is caught
        """

        with pytest.raises(AssertionError, match=r"must be str"):
            seg1d.algorithm.combine_corr(self.x, w)
