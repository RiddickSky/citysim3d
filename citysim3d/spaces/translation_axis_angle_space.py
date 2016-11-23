import numpy as np
from citysim3d.spaces import ConcatenationSpace, BoxSpace, AxisAngleSpace


class TranslationAxisAngleSpace(ConcatenationSpace):
    """
    SE(3) space where the translation part is a box in R^3 and the rotation
    part is represented as an axis-angle vector in R^3 where its magnitude is
    constrained within an interval and the axis can optionally be constrained.
    If the axis is not constrained, then the absolute value of low and high
    for the angle should be equal to each other.
    """
    def __init__(self, low, high, axis=None, dtype=None):
        """
        high and low are bounds for the translation part and the angle magnitude
        """
        self.box_space = BoxSpace(low[:3], high[:3], dtype=dtype)
        self.axis_angle_space = AxisAngleSpace(low[3], high[3], axis=axis)
        super(TranslationAxisAngleSpace, self).__init__([self.box_space, self.axis_angle_space])
        self.low = np.append(self.box_space.low, self.axis_angle_space.low)
        self.high = np.append(self.box_space.high, self.axis_angle_space.high)
        # alias the corresponding slices of self.low and self.high
        self.box_space.low, self.box_space.high = self.low[:3], self.high[:3]
        self.axis_angle_space.low, self.axis_angle_space.high = self.low[3:], self.high[3:]
        assert self.low.shape == (4,)
        assert self.high.shape == (4,)

    @property
    def axis(self):
        return self.axis_angle_space.axis

    @axis.setter
    def axis(self, axis):
        self.axis_angle_space.axis = axis

    @property
    def dtype(self):
        return self.box_space.dtype
