# TODO add comments


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return " (" + str(self.x) + " , " + str(self.y) + ") "

    # TODO maybe move this out of point class
    @staticmethod
    def do_overlap(l1, r1, l2, r2) -> bool:
        """Returns true if two rectangles(l1, r1)
               and (l2, r2) overlap  """

        # To check if either rectangle is actually a line
        # For example  :  l1 ={-1,0}  r1={1,1}  l2={0,-1}  r2={0,1}
        # if l1.x == r1.x or l1.y == r1.y or l2.x == r2.x or l2.y == r2.y:
        # the line cannot have positive overlap
        # return False

        # If one rectangle is on left side of other
        if l1.x >= r2.x or l2.x >= r1.x:
            return False

        # This does suit as in our case
        # If one rectangle is above other
        # if r1.y >= l2.y or r2.y >= l1.y:
        #     return False

        return True
