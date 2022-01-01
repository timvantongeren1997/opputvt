import numpy as np
from tqdm import tqdm

from typing import Callable

class Border():
    """ Object bordering the area an ant can move in.
    2 dimensional border defined by equation<max_value.
    Here equation is a function which given x and y calculates the function value,
    which is limited by the max_value to form an area.
    """    
    def __init__(
        self, 
        equation:Callable, 
        max_value:int,
    ) -> None:
        """Initialization

        Args:
            equation (function): equation defining the border
            max_value (int): max value of the border
        """    
        self.eq = equation
        self.max_value = max_value

    def check_inside(
        self, 
        x:float, 
        y:float,
    ) -> bool:
        """Checks if a point defined by an x and y coordinate is within the border.

        Args:
            x (float): x value
            y (float): y value

        Returns:
            bool: True if point within border, False otherwise
        """           
        return (self.eq(x,y)<self.max_value)

class Ant():
    """Ant object used to store positional information and simulate steps.
    Here a step is defined as a move in a single direction.
    """    
    def __init__(
        self, 
        stepsize:float, 
        seconds_per_step:float,
    ) -> None:
        """Initialization

        Args:
            stepsize (float): Size of a single step of the ant
            seconds_per_step (float): [description]
        """    
        self.stepsize = stepsize
        self.seconds_per_step = seconds_per_step

        # initial position and time spend walking
        self.x = 0
        self.y = 0
        self.time = 0
    
    def random_step(
        self,
    ) -> None:
        """Simulate a single step in a random direction,
        updating the position of the ant using its stepsize, 
        and increasing the time spent by the time it takes the ant to move one step.
        """        
        draw = np.random.randint(4)
        if draw==0:
            self.x += self.stepsize
        elif draw==1:
            self.y += self.stepsize
        elif draw==2:
            self.x -= self.stepsize
        elif draw==3:
            self.y -= self.stepsize
        
        self.time += self.seconds_per_step

def main():
    # Equation and border of the actual question
    def equation(
        x:float,
        y:float,
    ) -> float:
        """Equation as given in the question.

        Args:
            x (float): x value
            y (float): y value

        Returns:
            float: equation value in (x,y)
        """    
        return ((x-2.5)/30)**2 + ((y-2.5)/40)**2

    border = Border(equation=equation, max_value=1)

    # Equation and border of Q1, used to test the program
    # def equation(
    #     x:float,
    #     y:float,
    # ) -> float:
    #     """Equation of a square.

    #     Args:
    #         x (float): x value
    #         y (float): y value

    #     Returns:
    #         float: equation value in (x,y)
    #     """    
    #     return np.abs(x+y) + np.abs(x-y)

    # border = Border(equation=equation, max_value=40)
    
    precision = .01 # Stepsize when estimating crossing point
    times = []
    epochs = 10_000
    
    for _ in tqdm(range(epochs)):
        ant = Ant(10, 1)

        prev_x, prev_y = 0,0

        # Once this fails, the ant has stepped outside of the border
        while border.check_inside(ant.x, ant.y):
            prev_x, prev_y = ant.x, ant.y
            ant.random_step()
        
        # check crossing direction, 
        # e.g. (x_dir,y_dir)=(-1,0) if the ant crossed to the west
        x_dir = np.sign(ant.x-prev_x)
        y_dir = np.sign(ant.y-prev_y)

        # Starting from the backtracked position
        cross_x, cross_y = prev_x, prev_y

        # We find the crossing coordinates of the ant with the above specified precision
        # Note that as we always take the point just before crossing as the crossing point
        # we have a bias in our estimate.
        while border.check_inside(cross_x, cross_y):
            cross_x += precision*x_dir
            cross_y += precision*y_dir
        
        time = np.sum([
            ant.time - ant.seconds_per_step, # Backtrack one step
            ant.seconds_per_step*(np.maximum(np.abs(cross_x-prev_x), np.abs(cross_y-prev_y))/ant.stepsize), # Move to just before the border
            .5*precision*ant.seconds_per_step, # Adjust for underestimating bias
        ])
        
        times.append(time)

    print(f"Average time to get to the food is {np.mean(times):.3f}")


if __name__=="__main__":
    main()