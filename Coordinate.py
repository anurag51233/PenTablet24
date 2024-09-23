import math
from typing import List, Any
import ast
from numpy import ndarray, dtype, floating

import numpy as np

from scipy.optimize import fsolve
from scipy.optimize import least_squares


class Coordinate:
    """coordinate finding"""

    def __init__(self):
        # Define the initial guess for the solution
        self.x0 = np.array([37.0, 20.0, 30.0])  # Adjust based on expected solution region

        # Define the point parameters (centers )
        self.xpos = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0]
        self.ypos = [0.0, 15.0, 30.0, 45.0]
        self.z0 = 0
        self.r = []

        self.r_index_list = []



    # Combine the sphere equations into a single function
    def solve_coordinate(self, x):

        res_list = []


        if x[2] < 0 or x[1] < 0 or x[0] < 0 or x[0] > 100 or x[1] > 100:
            # If z is negative, penalize the solution heavily to avoid this region
            return [1e10] * 3  # return large penalty if constraints are violated


        if len(self.r) > 0:
            for index in range(24):
                if self.r[index] > 0:
                    #get the index
                    res = ((x[0] - self.xpos[int(index % 6)]) ** 2
                           + (x[1] - self.ypos[int(index // 6) % len(self.ypos)]) ** 2
                           + (x[2]) ** 2
                           - (self.r[index]) ** 2)
                else:
                    res = 0

                res_list.append(res)
        return res_list


    def calc(self, data1: str):
        k = 1
        actual_list = ast.literal_eval(data1)

        self.r.clear()
        for i in range(24):
            self.r.append(k * actual_list[i])


        # Use fsolve to find the solution
        res1 = least_squares(self.solve_coordinate, self.x0)

        return res1.x



#data = ("[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15.52417, 0, 17.88854, 25.94224, 0, 0, 0, 15.49193, 0, 41.0]")
# Convert the string to an actual list


#coo = Coordinate()
#ref1 = coo.calc(data)


#print(ref1)

