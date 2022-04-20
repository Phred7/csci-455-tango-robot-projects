from tango_project_4_assignment_5.action_stategy import ActionStrategy


class Action:
    """
    Strategy Pattern Context.
    """

    def __init__(self, action_strategy: ActionStrategy) -> None:
        self._action_strategy: ActionStrategy = action_strategy

    @property
    def action_strategy(self) -> ActionStrategy:
        """
        Property representing the type of Concrete Strategy that this object contains a reference to.
        :return: The type of Concrete Strategy that this object contains a reference to.
        """
        return self._action_strategy

    @action_strategy.setter
    def action_strategy(self, action_strategy: ActionStrategy) -> None:
        """
        Allows the concrete strategy object to be replaced at runtime.
        param instrumentation_strategy: New concrete strategy object to replace with the current.
        :return: None.
        """
        if action_strategy is not None:
            self._action_strategy = action_strategy
        return

    def execute_action(self) -> None:
        """
        Method that calls the algorithm or process defined by the concrete strategy.
        :return: None.
        """
        print(f"Executing {self._action_strategy.type}")
        self._action_strategy.execute_action()
        print(f"Execution of {self._action_strategy.type} complete")


