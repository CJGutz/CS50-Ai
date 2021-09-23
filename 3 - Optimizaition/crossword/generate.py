import sys
import numpy as np 

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3(None)
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        
        for var in self.domains.keys():
            for word in list(self.domains[var])[:]:
                if not len(word) == var.length:
                    self.domains[var].remove(word)            


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revised = False
        if self.crossword.overlaps[(x,y)] is not None:

            for x_word in list(self.domains[x])[:]:
                one_word_equal = False
                for y_word in self.domains[y]:
                    
                    x_index, y_index = self.crossword.overlaps[(x,y)] # Muligens (x, y)

                    if x_word[x_index] == y_word[y_index]:
                        one_word_equal = True

                if not one_word_equal:
                    self.domains[x].remove(x_word)
                    revise = True
        return revised
    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # only if arcs is None
        arcs = list(self.crossword.overlaps) if arcs is None else arcs
        
        # make variables in queue arc consistent
        while len(arcs) > 0:
            x, y = arcs.pop()
            if self.revise(x,y):
                if self.domains[x] == 0:
                    return False
                for key in set(self.crossword.overlaps.keys()):
                    if x in key and y not in key:
                        arcs.append(key)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        if len(assignment) < len(self.domains):
            return False        

        for value in assignment.values():
            if len(value) == 0:
                return False
        return True



    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for count, key in enumerate(assignment.keys()):
            if assignment[key] in set(assignment.values()) and not count == list(assignment.values()).index(assignment[key]):
                return False
            if not key.length == len(assignment[key]):
                return False
            for neighbor in list(self.crossword.neighbors(key)):
                x, y = self.crossword.overlaps[(key, neighbor)]
                for var in assignment.keys():
                    if var == neighbor:
                        if not assignment[key][x] == assignment[var][y]:
                            return False
        return True                     
            
            

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        domains = []
        conflicts = dict()
        for key in self.domains.keys():
            if not key is None and not key is var:
                overlap = self.crossword.overlaps[(var, key)]
                x, y = overlap if not overlap is None else (0,0)
                for value in self.domains[var]:
                    nr_of_conflicts = 0
                    for value2 in self.domains[key]:
                        if not value[x] == value2[y]:
                            nr_of_conflicts += 1
                    conflicts[value] = nr_of_conflicts

        sorted_list = sorted(conflicts.items(), key = lambda x : x[1], reverse=False)

        for domain in sorted_list:
            domains.append(domain[0])

        return domains


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned = None
        nr_of_values = 1000
        nr_of_neighbors = 0
        for var in self.domains.keys():
            if not var in set(assignment.keys()):
                if nr_of_values > len(self.domains[var]):
                    if nr_of_neighbors < len(self.crossword.neighbors(var)):
                        unassigned = var
                        nr_of_values = len(self.domains[unassigned])

        return unassigned


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """


        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        domains = self.order_domain_values(var, assignment)

        for value in domains:
            assignment[var] = value
            if self.consistent(assignment):

                result = self.backtrack(assignment)
                if not result is None:
                    return result
                assignment.pop(var)
            else:
                assignment.pop(var)
        return None


def main():


    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
