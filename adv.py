from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from timeit import default_timer as timer

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


####################################### OLD SOLUTION #######################################

# print(world.rooms)
# print(len(world.rooms))

# # set up the global variables
# global_done = False
# backup_light = False

# def find_a_path():

#     # Main recursion function
#     def path_recursion(visited={}, path=[], current_room=world.starting_room):
#         # if a path has been found, stop the function
#         global global_done
#         global traversal_path
#         global backup_light
        
#         if global_done == True or backup_light == True:
#             pass
#         else:
#             # check if your current room is inside the visited dictionary
#             # if it's not, add it, if it is, iterate local room visited counter
#             new_visited = visited.copy()

#             if current_room.id in visited:
#                 new_visited[current_room.id] += 1
#             else:
#                 new_visited[current_room.id] = 1

#             # if the visited dictionary contains all of the world rooms, stop the script and print the path
#             if len(new_visited) >= len(world.rooms):
#                 global_done = True
#                 print(f"The path is finished and we have visited {len(new_visited)} rooms")
#                 print(f"the path took {len(path)} steps")
#                 traversal_path = path

#             else:
#                 # get a list of exits from your current position
#                 current_exits = current_room.get_exits()

#                 # get a list of the actual rooms based on the exits provided
#                 adjacent_rooms = []
#                 for direction in current_exits:
#                     if direction == "n":
#                         # adjacent_rooms.append(("n", current_room.n_to))
#                         try:
#                             adjacent_rooms.append({'direction': 'n', 'room': current_room.n_to, 'times_visited': new_visited[current_room.n_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'n', 'room': current_room.n_to, 'times_visited': 0})
#                     elif direction == "s":
#                         try:
#                             adjacent_rooms.append({'direction': 's', 'room': current_room.s_to, 'times_visited': new_visited[current_room.s_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 's', 'room': current_room.s_to, 'times_visited': 0})
#                     elif direction == "e":
#                         try:
#                             adjacent_rooms.append({'direction': 'e', 'room': current_room.e_to, 'times_visited': new_visited[current_room.e_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'e', 'room': current_room.e_to, 'times_visited': 0})
#                     elif direction == "w":
#                         try:
#                             adjacent_rooms.append({'direction': 'w', 'room': current_room.w_to, 'times_visited': new_visited[current_room.w_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'w', 'room': current_room.w_to, 'times_visited': 0})
                
#                 # sort the adjacent rooms by times visited
#                 try:
#                     def visited_key(e):
#                         return e['times_visited']
#                     adjacent_rooms.sort(key=visited_key)
#                 except:
#                     print(f"Sorting failed. Adjacent rooms were: {adjacent_rooms}.\nCurrent path was length {len(path)}.\nVisited was {len(new_visited)}")

#                 # if the backup_light is off...
#                 if backup_light == False:
#                     # check for rooms which have not been visited
#                     unvisited_rooms = []
#                     for room_dict in adjacent_rooms:
#                         if room_dict['room'].id not in new_visited:
#                             unvisited_rooms.append(room_dict)
                    
#                     # if there are adjacent unvisited rooms, rerun the recursion for those rooms
#                     if len(unvisited_rooms) > 0:
#                         for room_dict in unvisited_rooms:
#                             new_path = path + [room_dict['direction']]
#                             new_room = room_dict['room']
#                             path_recursion(new_visited, new_path, new_room)
                    
#                     # if there are no adjacent unvisited rooms, turn the backup light on and search for a new room
#                     else:
#                         backup_light = True
#                         # search for a room with adjacent unvisited
#                         search_results = find_unvisited(new_visited, path, current_room)
#                         # if search results come up with nothing, pass
#                         if search_results is None:
#                             pass
#                         # rerun recursion at searched room
#                         else:
#                             # print(f"found a new room! Room {search_results[2].id}")
#                             path_recursion(search_results[0], search_results[1], search_results[2])

#     # helper function to find an unvisited room
#     def find_unvisited(visited, path, current_room):
#         global backup_light

#         if backup_light == False:
#             pass
#         else:
#             # get a list of exits from your current position
#             current_exits = current_room.get_exits()

#             # get a list of the actual rooms based on the exits provided
#             adjacent_rooms = []
#             for direction in current_exits:
#                     if direction == "n":
#                         # adjacent_rooms.append(("n", current_room.n_to))
#                         try:
#                             adjacent_rooms.append({'direction': 'n', 'room': current_room.n_to, 'times_visited': visited[current_room.n_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'n', 'room': current_room.n_to, 'times_visited': 0})
#                     elif direction == "s":
#                         try:
#                             adjacent_rooms.append({'direction': 's', 'room': current_room.s_to, 'times_visited': visited[current_room.s_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 's', 'room': current_room.s_to, 'times_visited': 0})
#                     elif direction == "e":
#                         try:
#                             adjacent_rooms.append({'direction': 'e', 'room': current_room.e_to, 'times_visited': visited[current_room.e_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'e', 'room': current_room.e_to, 'times_visited': 0})
#                     elif direction == "w":
#                         try:
#                             adjacent_rooms.append({'direction': 'w', 'room': current_room.w_to, 'times_visited': visited[current_room.w_to.id]})
#                         except:
#                             adjacent_rooms.append({'direction': 'w', 'room': current_room.w_to, 'times_visited': 0})

#             # sort the rooms by times visited
#             try:
#                 def visited_key(e):
#                     return e['times_visited']
#                 adjacent_rooms.sort(key=visited_key)
#             except:
#                 print(f"Helper sort failed. Adjacent rooms were: {adjacent_rooms}.\nCurrent path was length {len(path)}.\nVisited was {len(visited)}")
            
#             # check for rooms which have not been visited
#             unvisited_rooms = []
#             for room_dict in adjacent_rooms:
#                 if room_dict['room'].id not in visited:
#                     unvisited_rooms.append(room_dict)

#             # if there are adjacent unvisited rooms, return the current room and the path
#             if len(unvisited_rooms) > 0:
#                 backup_light = False
#                 return ([visited, path, current_room])
#             else:
#                 for room_dict in adjacent_rooms:
#                     new_path = path + [room_dict['direction']]
#                     new_room = room_dict['room']
#                     new_visited = visited.copy()
#                     new_visited[room_dict['room'].id] += 1
#                     # print(f"Current room is {current_room.id}. Moving to {new_room.id}. #visited is {new_visited}")
#                     return find_unvisited(new_visited, new_path, new_room)

#     path_recursion()

# find_a_path()

####################################### NEW SOLUTION #######################################

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

def bft_path():
    # Create a queue and enqueue the starting room
    qq = Queue()
    # Set up the dictionary
    starting_dict = {'visited': {world.starting_room.id: 1}, 'path': [], 'current_room': world.starting_room, 'visited_length': 1}

    # get a list of all the room ids
    world_room_ids = []
    for room in world.rooms:
        world_room_ids.append(room)
    print(world_room_ids)

    qq.enqueue(starting_dict)

    # Loop
    while True:
        # shorten the queue if it's too long
        # first sort the queue to favor the elements with the greatest "visited_length" - since those have been to the most rooms
        # then, shrink the queue to a managable size
        # 10,000 / 5,000 gets you 1,276 moves
        if len(qq.queue) > 10000:
            def visited_length(e):
                return e['visited_length']
            qq.queue.sort(key=visited_length, reverse=True)
            qq.queue = qq.queue[:5000]
            print(f"shrinking queue. New visited length is {qq.queue[0]['visited_length']}, path length is {len(qq.queue[0]['path'])} and time is {timer()}")
        
        # if qq.queue[0]['visited_length'] >= 468 and len(world_room_ids) >= 499:
        #     for number in qq.queue[0]['visited'].keys():
        #         if number in world_room_ids:
        #             world_room_ids.remove(number)
        #     print(world_room_ids)
        
        # dequeue / pop the first vertex
        current_data = qq.dequeue()


        # check if the current data has found a complete path
        if current_data['visited_length'] >= len(world.rooms):
            # if so, set the traversal path to the found path
            global traversal_path
            traversal_path = current_data['path']
            break

        # get a list of exits
        current_exits = current_data['current_room'].get_exits()

        # get a list of the actual rooms based on the exits - along with their direction and times visited
        adjacent_rooms = []
        for direction in current_exits:
            if direction == "n":
                new_room = current_data['current_room'].n_to
                try:
                    adjacent_rooms.append({ 'direction': 'n', 'room': new_room, 'times_visited': data_dict['visited'][new_room] })
                except:
                    adjacent_rooms.append({ 'direction': 'n', 'room': new_room, 'times_visited': 0 })
            elif direction == "s":
                new_room = current_data['current_room'].s_to
                try:
                    adjacent_rooms.append({ 'direction': 's', 'room': new_room, 'times_visited': data_dict['visited'][new_room] })
                except:
                    adjacent_rooms.append({ 'direction': 's', 'room': new_room, 'times_visited': 0 })
            elif direction == "e":
                new_room = current_data['current_room'].e_to
                try:
                    adjacent_rooms.append({ 'direction': 'e', 'room': new_room, 'times_visited': data_dict['visited'][new_room] })
                except:
                    adjacent_rooms.append({ 'direction': 'e', 'room': new_room, 'times_visited': 0 })
            elif direction == "w":
                new_room = current_data['current_room'].w_to
                try:
                    adjacent_rooms.append({ 'direction': 'w', 'room': new_room, 'times_visited': data_dict['visited'][new_room] })
                except:
                    adjacent_rooms.append({ 'direction': 'w', 'room': new_room, 'times_visited': 0 })
                
        
        # sort the adjacent rooms by times visited
        def visited_key(e):
            return e['times_visited']
        adjacent_rooms.sort(key=visited_key)
        
        # enqueue the adjacent rooms
        for adj_dict in adjacent_rooms:
            # update the visited list for the new room
            new_visited = current_data['visited'].copy()
            try:
                new_visited[adj_dict['room'].id] += 1
            except:
                new_visited[adj_dict['room'].id] = 1
            # update the path
            new_path = current_data['path'] + [adj_dict['direction']]
            # compile the new data and enqueue it
            new_data = {'visited': new_visited, 'path': new_path, 'current_room': adj_dict['room'], 'visited_length': len(new_visited)}
            qq.enqueue(new_data)

bft_path()


















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




            

