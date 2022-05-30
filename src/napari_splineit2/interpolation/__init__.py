import numpy as np

from scipy.interpolate import CubicSpline


class CubicInterpolator(object):
    
    def __init__(self,closed):
        self.closed = closed

    def __call__(self, ctrl_points):
        if ctrl_points.shape[0] < 3:
            ret =  ctrl_points.copy()
            if self.closed:
                first_point = ctrl_points[0,:]
                np.concatenate([ctrl_points, first_point[None,:]], axis=0)
        else:

            t = np.arange(ctrl_points.shape[0])
            cs_x = CubicSpline(t, ctrl_points[:,0])
            cs_y = CubicSpline(t, ctrl_points[:,1])
            tfine = np.linspace(0, t[-1])
            xx = cs_x(tfine)[:,None]
            yy = cs_y(tfine)[:,None]

            return np.concatenate([xx, yy], axis=1)




if __name__ == "__main__":
    
    ctrl_points = np.array([
        (10,10),
        (30, 10),
        (30, 30)

    ])


    ip = CubicInterpolator(closed=True)

    interpolated = ip(ctrl_points)

    print(interpolated)