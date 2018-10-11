"""
Abstract base class for State implementations.
"""
import builtins

from abc import ABCMeta, abstractmethod
from napari.core.typing import RegistryDecorator, List, Dict, Optional, Type

from .types import ExtractFunc, PopulateFunc, IncompatibilityError


state_ABCs = []


class State(metaclass=ABCMeta):
    """Abstract base class for a State.

    States are the main data objects that are passed between functions.

    States can be created by inheriting from this class or declaring an
    existing type a State with ``State.register(type)``.
    """
    def __new__(cls, *args, **kwargs):
        """Prevent direct class instantiation.
        """
        if cls in state_ABCs:
            raise TypeError(f'Cannot instantiate abstract base class {cls}')
        return super().__new__(cls, *args, **kwargs)


class DynamicStateMeta(ABCMeta, type):
    """Metaclass to create a class with non-inherited class variables.
    """
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class.extract_registry: Dict[Type, ExtractFunc] = dict()
        new_class.populate_registry: Dict[Type, PopulateFunc] = dict()

        return new_class


class DynamicState(State, metaclass=DynamicStateMeta):
    """Abstract base class for a DynamicState.

    A DynamicState is similar to a State but additionally provides methods
    to register and use conversion functions between it and other types.
    """

    @classmethod
    def register(cls, other_type: Type):
        """Disables registering.
        """
        raise NotImplementedError('Cannot register subclasses; '
                                  'use inheritance instead.')

    @classmethod
    def populates_with(cls) -> List[Type]:
        """Lists all types from which this state can be populated with.

        Returns
        -------
        compatible_types : list of type
            Types from which this state can be populated from.
        """
        return list(cls.populate_registry.keys())

    @classmethod
    def extracts_to(cls) -> List[Type]:
        """Lists all types which this state can be extracted to.

        Returns
        -------
        compatible_types : list of type
            Types which this state can be extracted to.
        """
        return list(cls.extract_registry.keys())

    @classmethod
    def add_populate_func(cls, obj_type: Type, func: PopulateFunc
                          ) -> Optional[PopulateFunc]:
        """Registers a function that populates a state given an object.

        Parameters
        ----------
        obj_type : type
            Type of the object which the function populates the state with.
        func : (State, object) -> State
            Function that populates a state given an object.

        Returns
        -------
        overwritten : (State, object) -> State or None
            Entry which was overwritten by this, if any.
        """
        overwritten = None
        try:
            overwritten = cls.populate_registry[obj_type]
        except KeyError:
            pass

        cls.populate_registry[obj_type] = func
        return overwritten

    @classmethod
    def add_extract_func(cls, obj_type: Type, func: ExtractFunc
                         ) -> Optional[ExtractFunc]:
        """Registers a function that extracts an object from a state.

        Parameters
        ----------
        obj_type : type
            Type of the object which the function will extract from the state.
        func : (State) -> object
            Function that extracts an object from a state.

        Returns
        -------
        overwritten : (State) -> object or None
            Entry which was overwritten by this, if any.
        """
        overwritten = None
        try:
            overwritten = cls.extract_registry[obj_type]
        except KeyError:
            pass

        cls.extract_registry[obj_type] = func
        return overwritten

    @classmethod
    def populate_func(cls, obj_type: Type
                      ) -> RegistryDecorator[PopulateFunc]:
        """Decorator for ``add_populate_func``.

        Parameters
        ----------
        obj_type : type
            Type of the object which the function populates the state with.

        Returns
        -------
        registry_decorator : registry_decorator of (State, object) -> State
            Decorator to register the populate function.
        """
        def registry_decorator(func: PopulateFunc) -> PopulateFunc:
            cls.add_populate_func(obj_type, func)
            return func

        return registry_decorator

    @classmethod
    def extract_func(cls, obj_type: Type) -> RegistryDecorator[ExtractFunc]:
        """Decorator for ``add_extract_func``.

        Parameters
        ----------
        obj_type : type
            Type of the object which the function will extract from the state.

        Returns
        -------
        registry_decorator : registry_decorator of (State) -> object
            Decorator to register the extract function.
        """
        def registry_decorator(func: ExtractFunc) -> ExtractFunc:
            cls.add_extract_func(obj_type, func)
            return func

        return registry_decorator

    @classmethod
    def populate_state_with(cls, state: State, obj: object) -> State:
        """Populates a state with the given object.

        Parameters
        ----------
        state : State
            State to be populated.
        obj : object
            Object to populate with.

        Returns
        -------
        state : State
            Populated state.

        Raises
        ------
        IncompatibilityError
            When no function was found to populate the state with the
            object type.
        """
        try:
            populate_func = cls.populate_registry[type(obj)]
            return populate_func(state, obj)
        except KeyError:
            raise IncompatibilityError(type(obj), cls) from None

    @classmethod
    def extract_state_to(cls, state: State, obj_type: Type) -> object:
        """Extracts data from a state to an object.

        Parameters
        ----------
        state : State
            State to extract from.
        obj_type : type
            Type of object to extract to.

        Returns
        -------
        obj : object
            Extracted object.

        Raises
        ------
        IncompatibilityError
            When no function was found to extract the object type from
            the state.
        """
        try:
            extract_func = cls.extract_registry[obj_type]
            return extract_func(state)
        except KeyError:
            raise IncompatibilityError(obj_type, cls) from None

    @classmethod
    def init_with(cls, obj: object) -> State:
        """Initializes a new instance using its ``default_init`` or
        ``__init__`` method with no arguments, then populates it with
        an object.

        Parameters
        ----------
        obj : object
            Object to populate with.

        Returns
        -------
        state : State
            New state.
        """
        try:
            init_func = cls.default_init
        except AttributeError:
            init_func = cls

        state = init_func()
        return cls.populate_state_with(state, obj)

    def populate_with(self, obj: object) -> State:
        """Populates the state with the given object.

        Parameters
        ----------
        obj : object
            Object to populate with.

        Returns
        -------
        state : State
            Populated state.

        Raises
        ------
        IncompatibilityError
            When no function was found to populate the state with the
            object type.
        """
        return self.populate_state_with(self, obj)

    def extract_to(self, obj_type: Type) -> object:
        """Extracts data from the state to an object.

        Parameters
        ----------
        obj_type : type
            Type of object to extract to.

        Returns
        -------
        obj : object
            Extracted object.

        Raises
        ------
        IncompatibilityError
            When no function was found to extract the object type from
            the state.
        """
        return self.extract_state_to(self, obj_type)


state_ABCs.extend([State, DynamicState])
