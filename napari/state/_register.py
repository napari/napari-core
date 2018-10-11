"""
State Registry.
"""
state_registry = list()


def register_state(state: 'State') -> 'State':
    """Registers a state.

    Parameters
    ----------
    state : State
        State to register.

    Returns
    -------
    state : State
        Registered state.
    """
    state_registry.append(state)
    return state
