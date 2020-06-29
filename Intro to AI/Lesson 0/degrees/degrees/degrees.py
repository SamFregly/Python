import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "small"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = '102' #person_id_for_name('Demi Lovato') #input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target =  '129' #person_id_for_name('Joe Jonas') #input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")



def goal(node):
    x = []
    while node.parent != None:
        x.append((node.action,node.state))
        node = node.parent
    print(x)
    return x

def shortest_path(source, target):
    q = 0                     # NEXT TIME TRY SORTING THE NEIGHBORS SET TO PRIORITIZE THOSE WITH THE MOST AVAILABLE ACTIONS
    print(source,target, 'start , end')
    frontier = QueueFrontier()
    actions = people[source]["movies"]
    for i in actions:
        frontier.add(Node(source,None,i))
    print(frontier.display(),'frontier')
    visited = QueueFrontier()
    neighbors = neighbors_for_person(source)
    ''' Repeat the below'''
    while True:
        ''' If Frontier is empty then no solution '''
        if frontier.empty():
            print('Broke')
            return None

        ''' Remove Node From Frontier'''
        cur = frontier.remove()
        neighbors = neighbors_for_person(cur.state)
        #print(neighbors,cur.state, 'Neighbors')

        '''If node contains goal state return the solution'''
        if cur.state == target:
            return goal(cur)

            ''' add node to the explored set'''
        else:
            q+=1
            visited.add(cur)
            #print(visited.display(),'VISITED')
            #print(cur.state, 'STATE',q,len(neighbors))
            ''' Expand node (current) add resulting nodes to the frontier if they arent in visited'''
            for action,state in neighbors:
                #print(action,state,'actions, state')
                if visited.contains_state(state) == False:
                    actions = people[state]["movies"]
                    #print(actions,'ACTIONS')
                    for i in actions:
                        new = Node(state,cur,i)
                        if new.state == target:
                            print('######')
                            return goal(new)
                        else:
                            frontier.add(new)
                else:
                    pass



#def get_actions(

def person_id_for_name(name): 
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
