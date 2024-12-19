#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code for CSCI-B551
#

import sys
import time

import copy
from queue import PriorityQueue

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    k, m, n = 30, 20, 10

    def parse_input(input_file):
        student_preferences = {}
        with open(input_file, 'r') as file:
            students = []
            preferred_team_sizes = []
            for line in file:
                parts = line.strip().split()
                student_id = parts[0]
                students.append(student_id)
                preferred_teammates = parts[1].split("-")
                requested_team_size = len(preferred_teammates)
                preferred_teammates = list(filter(lambda x: x != "zzz", preferred_teammates))
                preferred_team_sizes.append((student_id, requested_team_size))
                preferred_teammates.remove(student_id)
                excluded_students = parts[2].split(",")
                student_preferences[student_id] = [requested_team_size, preferred_teammates, excluded_students]
        return students, student_preferences, preferred_team_sizes

    # Checks if the goal state has been reached by verifying if all students are assigned to at least one team
    def is_goal(state):
        goal_reached = True
        assigned_students = []  # List to track students that have been assigned to teams
        
        # Step 1: Loop through each team in the current state (a list of teams)
        for team in state:
            # Step 2: Add each student in the team to the assigned_students list
            for student in team:
                assigned_students.append(student)
        
        # Step 3: Check if all students are assigned to at least one team
        for student in students:  # Loop through all students
            if student not in assigned_students:  # If a student is not assigned to any team
                return False  # Goal is not reached, return False
        
        return goal_reached  # All students are assigned to teams, return True
    
    # Add new team to the given list every time
    def add_new_group(state):
        # Step 1: Create a deep copy of the list of existing groups (teams) from the state
        list_of_groups = copy.deepcopy(state[1])
        
        # Step 2: Check if no teams exist, if so, create the first team with the first student
        if not list_of_groups:  # If the list of groups is empty
            list_of_groups.append([students[0]])  # Create a new team with the first student
        
        # Step 3: If there are existing teams, find an unassigned student and create a new team for them
        else:
            for student in students:
                found = False  # Flag to check if the student is already assigned to a team
                
                # Step 3.1: Check if the student is already part of any existing team
                for group in list_of_groups:
                    if student in group:
                        found = True
                        break  # If student is found in any group, exit the loop
                
                # Step 3.2: If the student is not assigned to any team, create a new team with that student
                if not found:
                    list_of_groups.append([student])
                    break  # Only add one unassigned student and stop adding further students
        
        # Step 4: Return the updated list of teams
        return list_of_groups
    
    def find_possible_team_members(list_of_groups):
        # Get the last group to be used for adding new team members
        group_to_be_made = list_of_groups[-1]
        used_students = set()  # A set to track all the used students
        
        # Collect all students that have been already assigned to groups
        for group in list_of_groups:
            for student in group:
                used_students.add(student)
        
        # Adding two-person teams
        two_person_groups = []
        for student in students:
            if student not in used_students:
                temp_list = [group_to_be_made[0], student]
                if sorted(temp_list) not in two_person_groups:
                    two_person_groups.append(sorted(temp_list))

        # Adding three-person teams
        three_person_groups = []
        for group in two_person_groups:
            for student in students:
                if student not in used_students and student not in group:
                    temp_list = group + [student]
                    if sorted(temp_list) not in three_person_groups:
                        three_person_groups.append(sorted(temp_list))

        # Append new two-person and three-person groups to the original list
        list_of_groups.extend(two_person_groups)
        list_of_groups.extend(three_person_groups)

        return list_of_groups

    def successors_ucs(state):
        successors = []  # List to hold the successors (new groups)
        
        # Add a new group based on the current state
        list_of_groups = add_new_group(state)
        
        # Find possible team members (groups) that can be formed
        possible_new_groups = find_possible_team_members(list_of_groups)
        
        # For each possible new group, check if it's already in the current state
        for new_group in possible_new_groups:
            temp_group = copy.deepcopy(state[1])  # Create a deep copy of the current group state
            
            # If the new group is not already in the current state, append it to the temp group
            if new_group not in state[1]:
                temp_group.append(new_group)
                successors.append(temp_group)
        
        return successors
    
    # Gets the preferred team size if the student name is given
    def find_desired_team_size(student_name):
        return student_preferences[student_name][0]

    # Gets the preferred team members as a list if the student name is given
    def find_desired_team_members(student_name):
        return student_preferences[student_name][1]

    # Gets the not preferred team members if the student name is given
    def find_not_desired_team_members(student_name):
        return student_preferences[student_name][2]
    
    def cost_function(teams):
        cost = 0
        # print("=============TEAMS=============")
        # print(f'teams: {teams}')
        for team in teams:
            cost = cost + k
            for teammember in team:
                teammember_preference = student_preferences[teammember]
                # incorrect team size
                if len(team) != teammember_preference[0]:
                    cost = cost + 1

                # did not get preferred teamates
                for preferred_teammate in teammember_preference[1]:
                    if preferred_teammate not in team:
                        cost = cost + n
                        # print(f'Preffered Teammate for {teammember}: {preferred_teammate}, Cost: {cost}')

                # got excluded teammates
                for excluded_teammate in teammember_preference[2]:
                    if excluded_teammate in team:
                        cost = cost + m
        #         print(f'Team member: {teammember}, Cost: {cost}')
        # print("==========================")
        return cost

    students, student_preferences, preferred_team_sizes = parse_input(input_file)


    fringe = PriorityQueue()
    initial_groups = []
    fringe.put((1, initial_groups))

    goal_states = []

    while fringe.qsize() > 0:
        popped = fringe.get()
        for s in successors_ucs(popped):
            if is_goal(s):
                result = {}
                result["assigned-groups"] = ["-".join(team) for team in s]
                result["total-cost"] = cost_function(s)
                goal_states.append(result)
                yield(goal_states[0])
            fringe.put((cost_function(s), s))

    return goal_states[0]

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])