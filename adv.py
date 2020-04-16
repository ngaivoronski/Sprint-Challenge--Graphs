from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


########## SOLUTION ##########

# print(world.rooms)
# print(len(world.rooms))

# set up the global variables
global_done = False
backup_light = False

def find_a_path():

    # Main recursion function
    def path_recursion(visited={}, path=[], current_room=world.starting_room):
        # if a path has been found, stop the function
        global global_done
        global traversal_path
        global backup_light
        
        if global_done == True or backup_light == True:
            pass
        else:
            # check if your current room is inside the visited dictionary
            # if it's not, add it, if it is, iterate local room visited counter
            new_visited = visited.copy()

            if current_room.id in visited:
                new_visited[current_room.id] += 1
            else:
                new_visited[current_room.id] = 1

            # if the visited dictionary contains all of the world rooms, stop the script and print the path
            if len(new_visited) >= len(world.rooms):
                global_done = True
                print(f"The path is finished and we have visited {len(new_visited)} rooms")
                print(f"the path took {len(path)} steps")
                traversal_path = path

            else:
                # get a list of exits from your current position
                current_exits = current_room.get_exits()

                # get a list of the actual rooms based on the exits provided
                adjacent_rooms = []
                for direction in current_exits:
                    if direction == "n":
                        adjacent_rooms.append(("n", current_room.n_to))
                    elif direction == "s":
                        adjacent_rooms.append(("s", current_room.s_to))
                    elif direction == "e":
                        adjacent_rooms.append(("e", current_room.e_to))
                    elif direction == "w":
                        adjacent_rooms.append(("w", current_room.w_to))
                
                # shuffle the adjacent rooms for randomness
                try:
                    random.shuffle(adjacent_rooms)
                except:
                    print(f"Shuffle failed. Adjacent rooms were: {adjacent_rooms}.\nCurrent path was length {len(path)}.\nVisited was {len(new_visited)}")

                # if the backup_light is off...
                if backup_light == False:
                    # check for rooms which have not been visited
                    unvisited_rooms = []
                    for room_tuple in adjacent_rooms:
                        if room_tuple[1].id not in new_visited:
                            unvisited_rooms.append(room_tuple)
                    
                    # if there are adjacent unvisited rooms, rerun the recursion for those rooms
                    if len(unvisited_rooms) > 0:
                        for room_tuple in unvisited_rooms:
                            new_path = path + [room_tuple[0]]
                            new_room = room_tuple[1]
                            path_recursion(new_visited, new_path, new_room)
                    
                    # if there are no adjacent unvisited rooms, turn the backup light on and search for a new room
                    else:
                        backup_light = True
                        # search for a room with adjacent unvisited
                        search_results = find_unvisited(new_visited, path, current_room)
                        # if search results come up with nothing, pass
                        if search_results is None:
                            pass
                        # rerun recursion at searched room
                        else:
                            print(f"found a new room! Room {search_results[2].id}")
                            path_recursion(search_results[0], search_results[1], search_results[2])

    # helper function to find an unvisited room
    def find_unvisited(visited, path, current_room):
        global backup_light

        if backup_light == False:
            pass
        else:
            # get a list of exits from your current position
            current_exits = current_room.get_exits()

            # get a list of the actual rooms based on the exits provided
            adjacent_rooms = []
            for direction in current_exits:
                if direction == "n":
                    adjacent_rooms.append(("n", current_room.n_to))
                elif direction == "s":
                    adjacent_rooms.append(("s", current_room.s_to))
                elif direction == "e":
                    adjacent_rooms.append(("e", current_room.e_to))
                elif direction == "w":
                    adjacent_rooms.append(("w", current_room.w_to))

            # shuffle the adjacent rooms for randomness
            try:
                random.shuffle(adjacent_rooms)
            except:
                print(f"Helper shuffle failed. Adjacent rooms were: {adjacent_rooms}.\nCurrent path was length {len(path)}.\nVisited was {len(visited)}")
            
            # check for rooms which have not been visited
            unvisited_rooms = []
            for room_tuple in adjacent_rooms:
                if room_tuple[1].id not in visited:
                    unvisited_rooms.append(room_tuple)

            # if there are adjacent unvisited rooms, return the current room and the path
            if len(unvisited_rooms) > 0:
                backup_light = False
                return ([visited, path, current_room])
            else:
                for room_tuple in adjacent_rooms:
                    new_path = path + [room_tuple[0]]
                    new_room = room_tuple[1]
                    new_visited = visited.copy()
                    new_visited[room_tuple[1].id] += 1
                    # print(f"Current room is {current_room.id}. Moving to {new_room.id}. #visited is {new_visited}")
                    return find_unvisited(new_visited, new_path, new_room)

    path_recursion()

find_a_path()
























# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")




            

