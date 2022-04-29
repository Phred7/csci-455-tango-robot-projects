from node_activity import NodeActivity


class Node:
    """
    Node.
    Strategy Pattern Context. Allows for the abstraction of the node_activity.
    """

    def __init__(self, node_name: str, node_activity: NodeActivity) -> None:
        self.node_activity_object: NodeActivity = node_activity
        self.node_name: str = node_name
        self.visited_bool: bool = False
        self.placed_in_map: bool = False

    def __str__(self) -> str:
        return f"Node({self.node_name})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def node_activity(self) -> NodeActivity:
        """
        Property representing the type of Concrete Strategy that this object contains a reference to.
        :return: The type of Concrete Strategy that this object contains a reference to.
        """
        return self.node_activity_object

    @node_activity.setter
    def node_activity(self, node_activity: NodeActivity) -> None:
        """
        Allows the concrete strategy object to be replaced at runtime.
        param instrumentation_strategy: New concrete strategy object to replace with the current.
        :return: None.
        """
        if node_activity is not None:
            self.node_activity_object = node_activity
        return

    def execute_node_activity(self) -> None:
        """
        Method that calls the algorithm or process defined by the concrete strategy.
        :return: None.
        """
        self.node_activity_object.node_activity()

    def visited(self) -> bool:
        return self.visited_bool

    def visit_node(self, *, define_visit: bool = None) -> None:
        """
        This method updates this Node to the visited state.
        :param define_visit: If this param is defined, it sets the state of the visited field. I.e. This param can set the visited state to False.
        :return: None.
        """
        self.visited_bool = define_visit if define_visit is not None else True


