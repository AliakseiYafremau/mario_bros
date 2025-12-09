class DomainError(Exception):
    """Custom exception for domain logic errors.

    This exception is raised whenever a rule of the game is
    violated (for instance, when a player is not on a valid floor
    or a conveyor is missing a next step). Ideally never called.
    """
    pass
