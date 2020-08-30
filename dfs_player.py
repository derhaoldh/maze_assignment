class Player:
    def __init__(self):
        """
        Attributes
        ----------
        self.frontier : list of Node object
            To store the unexplored node
        self.explored : str
            To store the explored node
        self.search_tree : list of dict
            To store the search tree that will update from time to time
        self.action : dict
            To translate the actions to the form of coordinates [x,y]
        """
        self.frontier = []
        self.explored = []
        self.action = ''
        self.search_tree = []
        self.id_counter = 1
        self.actions = {'n': [0, 1],
                        's': [0, -1],
                        'w': [-1, 0],
                        'e': [1, 0]
                        }

    def reset(self):
        """
             A function to reset all of the variable back to the initial state

             """
        self.id_counter = 1
        self.frontier = [Node(self.entrance["position"], None)]
        self.explored = []
        self.action = self.entrance["actions"]
        self.search_tree = []
        self.search_tree.append(
            {'id': 1, 'state': self.entrance["position"], 'children': [], 'actions': self.entrance["actions"],
             'removed': False, 'parent': None})

    def set_maze(self, maze, entrance, exits):
        """
             A function to initialize the initial state and actions

             """
        self.search_tree.append(
            {'id': 1, 'state': entrance["position"], 'children': [], 'actions': entrance["actions"], 'removed': False,
             'parent': None})
        self.action = entrance["actions"]
        self.maze = {
            "n_row": maze["n_row"],
            "n_col": maze["n_col"]
        }
        self.entrance = {
            "position": entrance["position"],
            "actions": entrance["actions"],
            "entrance": entrance["entrance"],
            "exit": entrance["exit"]
        }
        self.frontier.append(Node(self.entrance["position"], None))

    def next_node(self):
        """
            A function to create and return the next state

           Returns
           ------
           list
               a list of integer that represent the state
            """
        return self.dfs()

    def set_node_state(self, state):
        """
           A function to get the possible actions from the current state and
           to check whether the current state is an exit. If true, find the backtrace the state and
           return the solution of the path

           Returns
           ------
           List
               List of states that represent the solution from the initial state to the goal state
                    """
        self.action = state["actions"]
        if state['exit'] is True:
            goalie = self.frontier[0]
            path = [goalie.state]
            while goalie.parent is not None:
                path.insert(0, goalie.parent.state)
                for e in self.explored:
                    if e.state == goalie.parent.state:
                        goalie = e
                        break
            solution = {
                "found": True,
                "solution": path
            }
        else:
            solution = {
                "found": False,
                "solution": []
            }

        return solution

    def assignId(self):
        """
               A function to create a unique id for the value of id in the search tree

              Returns
              ------
              integer
                      an integer that represent the id
               """
        self.id_counter += 1
        return self.id_counter

    def updateTree(self, node, redundant=False):
        """
            A function to create a dict for each children for the search tree

            Returns
            ------
            dict
                the dict contains the key and value of the node
                     """
        temp = {'id': self.assignId(), 'state': node.state, 'children': [], 'actions': [], 'removed': False,
                'parent': 0}
        if node.parent is not None:
            for n in self.search_tree:
                if n['state'] == node.parent.state and n['removed'] is False:
                    temp['parent'] = n['id']
                    n['children'].append((temp['id']))
                    n['actions'] += str(node.action)

                if redundant is True:
                    temp['removed'] = True

        self.search_tree.append(temp)

    def dfs(self):
        """
            A function to represent the implementation of breath first search algorithm.

            """
        children = []
        actions = list(self.action)
        """
           Retrieve available actions of the current node
           """
        for action in actions:
            move = self.actions.get(action)
            """
                Translate the action to the list of integer [x,y]
                """
            new_position = [self.frontier[0].state[0] + move[0], self.frontier[0].state[1] + move[1]]
            """
               The new_position will derive from  [x+x,y+y] 
               """
            children.append(Node(new_position, self.frontier[0], str(action)))
            """
                 Create a Node object and append it into the list of children
                 """
        self.explored.append(self.frontier[0])
        del self.frontier[0]

        for child in children:
            if not (child.state in [e.state for e in self.explored]) and not (
                    child.state in [f.state for f in self.frontier]):
                """
                   if the state of of the child is not in explored and frontier list
                      """
                self.frontier.insert(0, child)
                self.updateTree(child)
            else:
                self.updateTree(child, True)

        return self.frontier[0].state

    def get_search_tree(self):
        """
               A function to return the search tree list to the frontend.

               """
        return self.search_tree


class Node:
    """
        A class used to represent a Node

        ...

        Attributes
        ----------
        self.state : list
            a list of integers that represents coordinates in the form of [x,y]
        self.parent : Node
            the node of parent of the node
        self.action : string
            the action of the parent node


        """

    def __init__(self, state=None, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
