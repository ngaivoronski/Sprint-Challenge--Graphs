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
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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

def find_a_path():

    def path_recursion(visited={}, path=[], current_room=world.starting_room, backup_light=False):
        # if a path has been found, stop the function
        global global_done
        global traversal_path
        
        if global_done == True:
            pass
        else:
            # check if your current room is inside the visited dictionary
            # if it's not, add it, if it is, iterate local room visited counter
            new_visited = visited.copy()

            if current_room in visited:
                new_visited[current_room] += 1
            else:
                new_visited[current_room] = 1

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
                        if room_tuple[1] not in new_visited:
                            unvisited_rooms.append(room_tuple)
                    
                    # if there are adjacent unvisited rooms, rerun the recursion for those rooms
                    if len(unvisited_rooms) > 0:
                        for room_tuple in unvisited_rooms:
                            new_path = path + [room_tuple[0]]
                            new_room = room_tuple[1]
                            path_recursion(new_visited, new_path, new_room, backup_light)
                    
                    # if there are no adjacent unvisited rooms, rerun the recursion with the backup_light on
                    else:
                        path_recursion(new_visited, path, current_room, True)
                
                # if the backup_light is off...
                else:
                    # check for rooms which have not been visited
                    unvisited_rooms = []
                    for room_tuple in adjacent_rooms:
                        if room_tuple[1] not in new_visited:
                            unvisited_rooms.append(room_tuple)

                    # if there are adjacent unvisited rooms, rerun the recursion for those rooms
                    # also turn the backup_light off
                    if len(unvisited_rooms) > 0:
                        for room_tuple in unvisited_rooms:
                            new_path = path + [room_tuple[0]]
                            new_room = room_tuple[1]
                            path_recursion(new_visited, new_path, new_room, False)
                    # if there are no unvisited adjacent rooms, rerun the recursion for all adjacent rooms with the backup_light on
                    else:
                        for room_tuple in adjacent_rooms:
                            new_path = path + [room_tuple[0]]
                            new_room = room_tuple[1]
                            path_recursion(new_visited, new_path, new_room, True)
                    
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




            

