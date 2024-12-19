#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code for CSCI-B551 
#


# !/usr/bin/env python3
import sys
import heapq
import math

# import csv
# def write_set_to_csv_row(visited_cities,city_gps_data,output_filename):
#     with open(output_filename, mode='w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(["City", "Latitude", "Longitude"])  # Header row

#         # Filter cities in the visited set and write their data to the CSV
#         for city in visited_cities:
#             if city in city_gps_data:
#                 latitude, longitude = city_gps_data[city]
#                 writer.writerow([city, latitude, longitude])


# FUNCTION TO RETURN THE LIST OF UNVISITED STATES
def get_unvisited_states(all_states_gps, visited_states):
    #Calculate the list of unvisited states, ignoring any extra states in visited_states.
    #all_states_gps (dict): Dictionary with state names as keys and GPS coordinates as values.
    #visited_states (set): Set of state names that have already been visited.
    # Get all states from the GPS dictionary keys
    all_states = set(all_states_gps.keys())   
    # Filter visited_states to only include states present in all_states
    valid_visited_states = visited_states & all_states    
    # Calculate unvisited states by subtracting valid visited states from all states
    unvisited_states = all_states - valid_visited_states    
    # Convert to a list (optional, for ordering or further processing)
    return list(unvisited_states)

# Function to calculate the average latitude and longitude for a missing city based on its neighbors
def calculate_avg_for_neighbors(city, roads_dict, city_gps,t_avg_lat,t_avg_long,avg_state_gps):
    total_lat = 0
    total_long = 0
    count = 0
    # Iterate over the neighboring cities of the given city
    for neighbor in roads_dict[city]:
        if neighbor in city_gps:  # Only consider neighbors with known GPS data
            lat, lon = city_gps[neighbor]
            total_lat += lat
            total_long += lon
            count += 1
    # Return the average if there are valid neighbors
    if count >= 3:
        avg_lat = total_lat / count
        avg_long = total_long / count
        return (avg_lat, avg_long)

    state_name = city.split(",_")[-1]
    if state_name in avg_state_gps:
        if avg_state_gps[state_name][2] >= 3:
        # Use state average if there are at least 3 cities in the state
            return (avg_state_gps[state_name][0], avg_state_gps[state_name][1])
    return (t_avg_lat,t_avg_long)  # Fallback for cities with no valid neighbors


def haversine(coords1, coords2):
    """
    Calculate the great-circle distance between two points on the Earth specified by latitude and longitude.
    Parameters:
    coords1 -- (lat1, lon1) tuple for the first point in decimal degrees
    coords2 -- (lat2, lon2) tuple for the second point in decimal degrees 
    Returns:    
    Distance between the two points in miles.
    """
    # Extract latitude and longitude from tuples
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    # Radius of Earth in miles
    R = 3958.8
    # Calculate the distance
    distance = R * c
    return distance

# Define cost functions based on various criteria (segments, distance, time, delivery) without heuristic

def cost_segments(fringe_hops):
    # taking the no of segments travelled from the start as cost function
    return fringe_hops + 1

def cost_distance(fringe_distance,current_distance):
    # taking the distance from the start as cost function
    return fringe_distance + current_distance

def cost_time(fringe_time,current_distance,speed_limit):
    # taking the total travel time from the start as cost function
    return fringe_time + current_distance/(speed_limit+5)

def cost_delivery(fringe_delivery,current_distance,speed_limit):
    # taking the total accidents possibility from the start as cost function
    return fringe_delivery + 0.000001 * speed_limit * current_distance

def state_tour_heuristic(haversine_distance, states_travelled, us_states_gps, city_lat_long, current_distance):
    # Get the list of unvisited states
    unvisited_states = get_unvisited_states(us_states_gps, states_travelled)    
    # Initial cost based on the number of unvisited states (penalty for each unvisited state)
    cost_ = len(unvisited_states) * 1000
    # Add current travel distance and the direct haversine distance to the destination
    cost_ = cost_ + current_distance + haversine_distance
    # Add the Haversine distance from the current city to each unvisited state
    for state in unvisited_states:
        state_coords = us_states_gps[state]
        cost_ = cost_ + haversine(city_lat_long, (state_coords[0], state_coords[1]))    
    return cost_

def cost_distance_heuristic(haversine_distance,fringe_distance,current_distance):
    # taking the total distance from the start plus straight line distance from the end state as cost function
    return haversine_distance + fringe_distance + current_distance

def cost_segments_heuristic(fringe_hops,haversine_distance):
    # taking the total segments from the start plus minimum possible segments from the end state as cost function
    return fringe_hops + 1 + int(haversine_distance/120)
    # 120 is chosen here because 99 percentile of distances of each segments is 118

def cost_time_heuristic(haversine_distance,max_speed,fringe_time,current_distance,speed_limit):
    # taking the total time taken from the start plus minimum time from the end state if we have a straignt road with max speed limit as cost function
    return fringe_time + current_distance/(speed_limit+5) + haversine_distance/(max_speed+5)    

def cost_delivery_heuristic(haversine_distance,min_speed,fringe_delivery,current_distance,speed_limit):
    # taking the total accident possibility from the start plus minimum possible accidents from the end state if we have a straignt road with min speed as cost function
    return fringe_delivery + 0.000001 * speed_limit * current_distance + 0.000001 * min_speed * haversine_distance

def cost_function_cal_heuristic(cost,current_fringe, current_distance, speed_limit,city_lat_long,end_city_lat_long,max_speed,min_speed,states_travelled,us_states_gps):
    # this function has the cost functions with heuristics
    # Calculate the great-circle distance between two points on the Earth specified by latitude and longitude.
    haversine_distance = haversine(city_lat_long,end_city_lat_long)
    if cost == 'segments':  
        return cost_segments_heuristic(current_fringe[2],haversine_distance)
    elif cost == 'distance':
        return cost_distance_heuristic(haversine_distance,current_fringe[3], current_distance)
    elif cost == 'time':
        return cost_time_heuristic(haversine_distance,max_speed,current_fringe[4], current_distance, speed_limit)
    elif cost == 'delivery':
        return cost_delivery_heuristic(haversine_distance,min_speed,current_fringe[5], current_distance, speed_limit)
    elif cost == 'tour':
        return state_tour_heuristic(haversine_distance, states_travelled, us_states_gps, city_lat_long, current_distance)

    


def cost_function_cal(cost,current_fringe, current_distance, speed_limit,city_lat_long,end_city_lat_long,max_speed,min_speed,states_travelled,us_states_gps):    
    if cost == 'segments': 
        return cost_segments(current_fringe[2])
    elif cost == 'distance': 
        return cost_distance(current_fringe[3], current_distance)
    elif cost == 'time': 
        return cost_time(current_fringe[4], current_distance, speed_limit)   
    elif cost == 'delivery': 
        return cost_delivery(current_fringe[5], current_distance, speed_limit)
    elif cost == 'tour':
        return state_tour_heuristic(haversine_distance, states_travelled, us_states_gps, city_lat_long, current_distance)


def get_route(start, end, cost):

    #create the useable data sets with input files. Using dictionary here since pandas availability in autograder is unknown

    # Initialize the dictionary to store the road segments
    roads_dict = {}
    max_speed = 0
    min_speed = 1000000000
    # Read the file and create the graph structure
    for line in open('road-segments.txt', 'r'):
        road_segment = line.split()
        # print(road_segment)
        # Unpack the data for better readability
        city1, city2, distance, speed_limit, road_name = road_segment
        distance = float(distance)
        speed_limit = float(speed_limit)
        if speed_limit > max_speed:
            max_speed = speed_limit
        if speed_limit < min_speed:
            min_speed = speed_limit
        # Initialize sub-dictionaries if the cities are not already in the dictionary
        if city1 not in roads_dict:
            roads_dict[city1] = {}
        if city2 not in roads_dict:
            roads_dict[city2] = {}
        # Add the road segment to the dictionary (bi-directional)
        roads_dict[city1][city2] = (distance, speed_limit, road_name)
        roads_dict[city2][city1] = (distance, speed_limit, road_name)

    # Initialize the dictionary to store the GPS coordinates for each city
    city_gps = {}
    state_gps = {}
    # Read the file and populate the dictionary
    avg_lat = 0
    avg_long = 0
    cnt = 0
    for line in open('city-gps.txt', 'r'):
        data = line.split()
        # Unpack the data for better readability
        city_name = data[0]
        latitude = float(data[1])
        longitude = float(data[2])
        # Store the GPS coordinates in the dictionary
        city_gps[city_name] = (latitude, longitude)
        avg_lat = avg_lat + latitude
        avg_long = avg_long + longitude
        cnt = cnt + 1
        # Extract state name (after the last ",_")
        state_name = city_name.split(",_")[-1]  
        if state_name not in state_gps:
            state_gps[state_name] = [0, 0, 0]  # Initialize latitude, longitude sums adn count for the state
        state_gps[state_name][0] = state_gps[state_name][0] + latitude
        state_gps[state_name][1] = state_gps[state_name][1] + longitude
        state_gps[state_name][2] = state_gps[state_name][2] + 1


    # Calculate the average GPS and store as a tuple (avg_lat, avg_long, count) for each state
    avg_state_gps = {
        state: (
            state_gps[state][0] / state_gps[state][2],   # Average latitude
            state_gps[state][1] / state_gps[state][2],   # Average longitude
            state_gps[state][2]                          # Number of cities
        ) for state in state_gps
    }

    avg_lat = avg_lat / cnt
    avg_long = avg_long / cnt

    # print(len(city_gps.keys()),len(roads_dict.keys()))
    # Identify cities that are in roads_dict but not in city_gps
    missing_cities = set(roads_dict.keys()) - set(city_gps.keys())

    # Add placeholder coordinates for missing cities
    for city in missing_cities:
        city_gps[city] = calculate_avg_for_neighbors(city, roads_dict, city_gps,avg_lat,avg_long,avg_state_gps)

    # print(len(city_gps.keys()),len(roads_dict.keys()))
    # 48 contiguous_usa_states
    usa_states = [
    'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 
    'Delaware', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 
    'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 
    'Nevada', 'New_Hampshire', 'New_Jersey', 'New_Mexico', 'New_York', 
    'North_Carolina', 'North_Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
    'Pennsylvania', 'Rhode_Island', 'South_Carolina', 'South_Dakota', 
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
    'West_Virginia', 'Wisconsin', 'Wyoming'
    ]

    us_states_gps = {state: avg_state_gps[state] for state in usa_states if state in avg_state_gps}

    current_city = start # initate the fringes with the start city
    current_path = [start] # keeping the track of the path taken
    visited_cities = set() # keeping the track of the cities visited to avoid loops
    city_cost_dict = {} # keeping the track of the best cost with which cities are visited to go in the best path
    end_city_lat_long = city_gps[end] # end city lat long 
    start_lat_long = city_gps[start] # start city lat long
    current_states = set()
    current_states.add(start.split(",_")[-1])
    total_segments = 0 # total segments/hops in the way
    total_distance = 0 # total distance in the way
    total_time = 0 # total time in the way
    total_delivery = 0 # total accidents in the way, named it delivey so that we have uniformity with the cost function text
    route_taken = [] # routes taken to be printed

    fringe = [] # fringes to carry on the iterations and search using A*
    #initial state at start city to be pushed to the fringe 
    start_state = (start,current_path, total_segments, total_distance, total_time, total_delivery,route_taken,current_states)

    #pushing start state to the fringe
    # we use the heap here instead of list necause of the better time complexity
    # heap : O(log(n)) for both push and pop
    # list : O(nlog(n)) for sorting, O(n) for pop
    heapq.heappush(fringe, (0, start_state))
    while fringe: #continue search when fringe is not empty
        current_cost, current_fringe = heapq.heappop(fringe) #retriving cost and state from the fringe
        current_city = current_fringe[0] #city in the fringe
        if current_city == end: # reached the end city
            # print(len(current_fringe[7]))
            # write_set_to_csv_row(visited_cities, city_gps,  "without_heuristics.csv")
            return {"total-segments": len(current_fringe[6]),
                    "total-miles": current_fringe[3],
                    "total-hours": current_fringe[4],
                    "total-expected-accidents": current_fringe[5],
                    "route-taken": current_fringe[6]}

        if current_city not in visited_cities: # add new city to the visited list
            visited_cities.add(current_city)
        elif current_cost > city_cost_dict[current_city]: # we visit the city again with a new path and better cost we explore this again
            continue
        city_cost_dict[current_city] = current_cost # adding the cost

        nearby_cities = roads_dict[current_city].keys() # get the neighbouring connections
        for next_city in nearby_cities:
            distance, speed_limit, road_name = roads_dict[current_city][next_city] # get the distance, speed_limit and route for this node to node connection
            next_city_lat_long = city_gps[next_city] # gps location of the next node
            next_city_segment = current_fringe[2] + 1 # segment number
            next_city_distance = current_fringe[3] + distance # total distance
            next_city_time = current_fringe[4] + distance/(speed_limit+5) # total travel time
            next_city_delivery = current_fringe[5] + 0.000001 * speed_limit * distance # total accidents possibility
            next_city_route_taken = current_fringe[6] + [(str(next_city), str(road_name) + " for " + str(distance) + " miles")] # routes to be taken
            next_states = current_fringe[7].copy()
            next_states.add(next_city.split(",_")[-1])
            #cost function with heuristics
            next_city_cost = cost_function_cal_heuristic(cost,current_fringe, distance, speed_limit,next_city_lat_long,end_city_lat_long,max_speed,min_speed,next_states,us_states_gps)

            #cost function without heuristics
            # next_city_cost = cost_function_cal(cost,current_fringe, distance, speed_limit,next_city_lat_long,end_city_lat_long,max_speed,min_speed,next_states,us_states_gps)

            if next_city not in visited_cities:
                heapq.heappush(fringe, (next_city_cost, (next_city, current_fringe[1]+[next_city],next_city_segment, next_city_distance, next_city_time, next_city_delivery,next_city_route_taken,next_states)))
            #add the next state if it is not visited already

            else:
                if next_city_cost < city_cost_dict[next_city]:
                    heapq.heappush(fringe, (next_city_cost, (next_city, current_fringe[1]+[next_city],next_city_segment, next_city_distance, next_city_time, next_city_delivery,next_city_route_taken,next_states)))
            #add the next state if it is visited already but we are seeing a better path to that state


    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-expected-accidents": a float indicating the expected (average) accidents
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    return False
    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    # return {"total-segments" : len(route_taken), 
    #         "total-miles" : 51., 
    #         "total-hours" : 1.07949, 
    #         "total-expected-accidents" : 1.1364, 
    #         "route-taken" : route_taken}






# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery","tour"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total expected accidents: %8.3f" % result["total-expected-accidents"])


