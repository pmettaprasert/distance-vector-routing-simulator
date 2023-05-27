"""
CPSC 5510, Seattle University, Project #3
:Author: Phubeth Mettaprasert
:Description: A common file where entities that represents routers are
defined. This simulates the sharing of costs between routers.
:Version: s23
"""

###############################
# NOTE THIS USES THE ACTUAL FORMULA IN KUROSE TEXTBOOK AND FOLLOWS THE ACTUAL
# BELLMAN-FORD ALGORITHM. SO THE NUMBER WILL BE DIFFERENT FROM WHAT PROFESSOR
# LUNDEEN GAVE IN HIS SAMPLE OUTPUT. IN SLACK HE SAID IT IS OK.
###############################

###############################
# ALSO I AM ATTEMPTING THE EXTRA CREDIT
###############################

# YOU MAY NOT ADD ANY IMPORTS
from entity import Entity
from student_utilities import to_layer_2

# global original costs this will only change when link cost changes
ORIGINAL_COSTS = [(0, 1, 3, 7),
                  (1, 0, 1, float('inf')),
                  (3, 1, 0, 2),
                  (7, float('inf'), 2, 0)]


def common_init(self):
    """
    You may call a common function like this from your individual __init__ 
    methods if you want.
    """


    # Initialize the distance table
    self.distance_table[self.node] = list(ORIGINAL_COSTS[self.node])

    print("Entity " + str(self.node) + " initializing")
    print(self)

    for neighbor in self.neighbors:
        to_layer_2(self.node, neighbor, self.distance_table[self.node])


def common_update(self, packet):
    """
    You may call a common function like this from your individual update 
    methods if you want.
    """

    # Update the distance table
    self.distance_table[packet.src] = packet.mincost

    # Keep track of whether distance table has been changed
    updated = False

    # To the destination node
    for dest_node in range(len(self.distance_table)):

        # Skip if the destination node is itself
        if dest_node == self.node:
            continue

        # create a list to use to find the minimum cost
        distance_to_dest = []
        for neighbor_node in range(len(self.distance_table)):

            # If the neighbor node is itself then it should be just the
            # cost of the direct path else we calculate the cost from self to
            # neighbor and neighbor to destination
            if neighbor_node == self.node:
                total_cost = ORIGINAL_COSTS[self.node][dest_node]
            else:
                cost_to_neighbor = ORIGINAL_COSTS[self.node][neighbor_node]
                cost_neighbor_to_dest = self.distance_table[neighbor_node][
                    dest_node]
                total_cost = cost_to_neighbor + cost_neighbor_to_dest
            distance_to_dest.append(total_cost)

        # Find the minimum cost
        min_cost = min(distance_to_dest)

        # If the minimum cost is different from the current cost then update
        if min_cost != self.distance_table[self.node][dest_node]:
            updated = True

        # Update the distance table
        self.distance_table[self.node][dest_node] = min_cost

    # If the distance table has been updated then send the update to neighbors
    if updated:
        for neighbor in self.neighbors:
            to_layer_2(self.node, neighbor, self.distance_table[self.node])

    # Printing out the different strings
    print("node " + str(self.node) + ": update from " + str(packet.src) + " "
                                                                          "received")
    if updated:
        print("Changes based on update")
    else:
        print("No changes in node " + str(self.node) + ", so nothing to do")

    print(self)

    if updated:
        print("sending mincost updates to neighbors\n")


def common_link_cost_change(self, to_entity, new_cost):
    """
    You may call a common function like this from your individual 
    link_cost_change methods if you want.
    Note this is only for extra credit and only required for Entity0 and 
    Entity1.
    """

    # Change the costs for the node and the node to the entity for original
    # for some reason the list way keeps changing so it has to be tuple at first
    modified_cost = list(ORIGINAL_COSTS[self.node])
    modified_cost2 = list(ORIGINAL_COSTS[to_entity])

    modified_cost[to_entity] = new_cost
    modified_cost2[self.node] = new_cost

    ORIGINAL_COSTS[self.node] = tuple(modified_cost)
    ORIGINAL_COSTS[to_entity] = tuple(modified_cost2)

    # Keep track of whether distance table has been changed
    updated = False

    # The algorithm is the same as the update.
    for dest_node in range(len(self.distance_table)):

        # Skip if the destination node is itself
        if dest_node == self.node:
            continue

        distance_to_dest = []
        for neighbor_node in range(len(self.distance_table)):

            # If the neighbor node is itself then it should be just the
            # cost of the direct path else we calculate the cost from self to
            # neighbor and neighbor to destination
            if neighbor_node == self.node:
                total_cost = ORIGINAL_COSTS[self.node][dest_node]
            else:
                cost_to_neighbor = ORIGINAL_COSTS[self.node][neighbor_node]
                cost_neighbor_to_dest = self.distance_table[neighbor_node][
                    dest_node]
                total_cost = cost_to_neighbor + cost_neighbor_to_dest

            # Add it to the end of the distance list.
            distance_to_dest.append(total_cost)

        # Find the minimum cost
        min_cost = min(distance_to_dest)
        if min_cost != self.distance_table[self.node][dest_node]:
            updated = True
        self.distance_table[self.node][dest_node] = min_cost

    if updated:
        for neighbor in self.neighbors:
            to_layer_2(self.node, neighbor, self.distance_table[self.node])

    print("Cost change in node " + str(self.node) + " to node " + str(
        to_entity))

    if updated:
        print("Changes based on update")
    else:
        print("No changes in node " + str(self.node) + ", so nothing to do")

    print(self)

    if updated:
        print("sending mincost updates to neighbors\n")


class Entity0(Entity):
    """Router running a DV algorithm at node 0"""

    def __init__(self):
        """
        Constructor for the entity. Define its own node number and its neighbors
        """
        super().__init__()
        self.node = 0
        self.neighbors = [1, 2, 3]
        common_init(self)

    def update(self, packet):
        """
        Updates the distance table for each entity.

        Params:
            packet: Packet object that contains the source node, destination
        """
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        """
        Accounts for the cost change. Changes the cost from self.node to the
        other entity
        Params:
            to_entity: The entity that the cost is changing to
            new_cost: The new cost that is changing to
        """
        common_link_cost_change(self, to_entity, new_cost)


class Entity1(Entity):
    """Router running a DV algorithm at node 1"""

    def __init__(self):
        """
        Constructor for the entity. Define its own node number and its neighbors
        """
        super().__init__()
        self.node = 1
        self.neighbors = [0, 2]
        common_init(self)

    def update(self, packet):
        """
        Updates the distance table for each entity.

        Params:
            packet: Packet object that contains the source node, destination
        """
        common_update(self, packet)

    def link_cost_change(self, to_entity, new_cost):
        """
        Accounts for the cost change. Changes the cost from self.node to the
        other entity
        Params:
            to_entity: The entity that the cost is changing to
            new_cost: The new cost that it is changing to
        """
        common_link_cost_change(self, to_entity, new_cost)


class Entity2(Entity):
    """Router running a DV algorithm at node 2"""

    def __init__(self):
        """
        Constructor for the entity. Define its own node number and its neighbors
        """
        super().__init__()
        self.node = 2
        self.neighbors = [0, 1, 3]
        common_init(self)

    def update(self, packet):
        """
        Updates the distance table for each entity.

        Params:
            packet: Packet object that contains the source node, destination
        """
        common_update(self, packet)


class Entity3(Entity):
    """Router running a DV algorithm at node 3"""

    def __init__(self):
        """
        Constructor for the entity. Define its own node number and its neighbors
        """
        super().__init__()
        self.node = 3
        self.neighbors = [0, 2]
        common_init(self)

    def update(self, packet):
        """
        Updates the distance table for each entity.

        Params:
            packet: Packet object that contains the source node, destination
        """
        common_update(self, packet)
