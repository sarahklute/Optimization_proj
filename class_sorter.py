from evo import Evo
import random as rnd
import pandas as pd
import numpy as np
from decorator import timer
import array as arr
import time
import random

# importing csvs
sections = pd.read_csv('sections.csv')
tas = pd.read_csv('tas.csv')


# OBJECTIVES

# minimize overallocation of TAs
## max_assigned labs
### penelty occurs if over assigning them to labs (if they request at most 2, any more is over)
def overallocation(assignment):
    ''' penelty occurs if over assigning them to labs (if they request at most 2,
    any more is over)
    '''
    overAllocated = np.sum(assignment, axis=1) - tas.max_assigned
    return sum(overAllocated[overAllocated > 0])


# minimize time conflicts
## cant be assigned two labs at the same time (look in section file)
## all time conflicts = 1 (dont double count)
def time_conf(assignment):
    ''' penelty occurs if two tas are assigned to two labs at the same time
    '''
    conflicts = 0
    df_assignment = pd.DataFrame(assignment)

    for slot in sections['daytime'].unique():
        df_slot = sections[sections['daytime'] == slot]

        for _, ta_row in df_assignment.iterrows():
            # Extract the relevant columns using loc
            ta_subset = ta_row.loc[df_slot.index]

            # Check for conflicts
            if ta_subset.sum() > 1:
                conflicts += 1
    return conflicts



# minimize under-support
## lab needs 3 tas, need that many or penalty for every one under
def under_sup(assignment):

    assignment_df = pd.DataFrame(assignment)

    total_penalty = 0

    for i, section in enumerate(sections.itertuples()):
        min_ta_required = section.min_ta
        #print("min ta", min_ta_required)
        ta_count = assignment_df[i].sum()
        #print("ta count", ta_count)
        under_support = max(0, min_ta_required - ta_count)   # Penalize for assigning too few TAs
        total_penalty += under_support


    return total_penalty



# minimize unwillingness
## number of times ta gets assigned section that they are U to be in
def unwill(assignment):

    selected_columns = tas.iloc[:, 3:]
    replacement_dict = {'U': 1, 'P': 0, 'W': 0}
    ta_array = selected_columns.replace(replacement_dict).values
    unwilling_assignments = ((assignment + ta_array) == 2).sum()

    return unwilling_assignments

# minimize willing but not prefered (unprefered)
## in sections they prefer
### create an unprefered column in tas
def unpref(assignment):

    selected_columns = tas.iloc[:, 3:]
    replacement_dict = {'U': 0, 'P': 0, 'W': 1}
    ta_array = selected_columns.replace(replacement_dict).values
    unpreferred_assignments = ((assignment + ta_array) == 2).sum()

    return unpreferred_assignments



# AGENTS
def swapper(solutions):
    """ Agent: An agent to modify an existing solution """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L


def toggle(solutions):
    """ Agent: Toggles the values of preferred and unpreferred assignments """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L[0]))  # Assuming L is a 2D array

    # Toggle the values at the selected position
    L[i][j] = 1 - L[i][j]

    return L

def remove(solutions):
    """ Agent: Removes assignments of TAs who are unwilling """
    L = solutions[0]
    num_tas, num_sections = len(L), len(L[0])

    for i in range(num_tas):
        for j in range(num_sections):
            if L[i][j] == 1:  # If TA is assigned
                # Assuming unwillingness is represented by 1 (you may need to adjust this based on your data)
                if tas.iloc[i, j + 3] == 'W':  # Check if TA is unwilling
                    L[i][j] = 0  # Unassign the unwilling TA

    return L


def extract(solutions):
    """ Agent: Extracts a random area from one solution and applies it to another """
    num_solutions = len(solutions)

    # Select two random solutions
    solution_a = solutions[rnd.randrange(0, num_solutions)]
    solution_b = solutions[rnd.randrange(0, num_solutions)]

    # Extract a random area from solution_a
    rows, cols = len(solution_a), len(solution_a[0])
    start_row = rnd.randrange(0, rows)
    start_col = rnd.randrange(0, cols)
    end_row = rnd.randrange(start_row + 1, rows + 1)
    end_col = rnd.randrange(start_col + 1, cols + 1)

    # Apply the extracted area to solution_b
    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            solution_b[i][j] = solution_a[i][j]

    return solution_b

def flip(solutions):
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i, j] = 1 - L[i,j]

@timer
def main():
    # Creating an instance of the framework
    E = Evo()

    # Register all objectives (fitness criteria)
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("time_conflicts", time_conf)
    E.add_fitness_criteria("undersupport", under_sup)
    E.add_fitness_criteria("unwilling_assignments", unwill)
    E.add_fitness_criteria("unpreferred_assignments", unpref)


    # Register all the agents
    E.add_agent("swapper", swapper, 1)

    # Initialize the population
    sections = pd.read_csv('sections.csv')
    tas = pd.read_csv('tas.csv')

    num_tas = len(tas['ta_id'])
    num_sections = len(sections['section'])

    # Create a 2D array initialized with all 0s
    array = np.zeros((num_tas, num_sections), dtype=int)

    # Randomly assign 1s to represent TAs not assigned to a section
    for row in array:
        unassigned_sections = random.sample(range(num_sections), random.randint(1, num_sections))
        for section in unassigned_sections:
            row[section] = 1

    assignment = array
    E.add_solution(assignment) #curently calling and printing out solution

    # Display population summary
    print(E)

    # Run the solver
    E.evolve(n=1, dom=100, time_limit=600) # dom is the number of domminent solutions, which solutions to keep

    print(E)



main()