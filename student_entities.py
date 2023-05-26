"""
CPSC 5510, Seattle University, Project #3
:Author: student # FIXME fill in _your_name
:Version: s23
"""

# YOU MAY NOT ADD ANY IMPORTS
from entity import Entity
from student_utilities import to_layer_2


def common_init(self):
    """
    You may call a common function like this from your individual __init__ 
    methods if you want.
    """
    pass  # FIXME (optional)


def common_update(self, packet):
    """
    You may call a common function like this from your individual update 
    methods if you want.
    """
    pass  # FIXME


def common_link_cost_change(self, to_entity, new_cost):
    """
    You may call a common function like this from your individual 
    link_cost_change methods if you want.
    Note this is only for extra credit and only required for Entity0 and 
    Entity1.
    """
    pass  # FIXME (optional)


class Entity0(Entity):
    """Router running a DV algorithm at node 0"""
    pass  # FIXME


class Entity1(Entity):
    """Router running a DV algorithm at node 1"""
    pass  # FIXME


class Entity2(Entity):
    """Router running a DV algorithm at node 2"""
    pass  # FIXME


class Entity3(Entity):
    """Router running a DV algorithm at node 3"""
    pass  # FIXME
