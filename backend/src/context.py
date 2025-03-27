import functools
import inspect
from typing import Any, get_type_hints


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if wrapper.instance is None:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance

    wrapper.instance = None

    return wrapper


def inject(original_function):
    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        context = ApplicationContext()

        argument_type_hints = get_type_hints(original_function)

        argument_specification = inspect.getfullargspec(original_function)
        argument_defaults = argument_specification.defaults or ()
        keyword_arguments = argument_specification.args[-len(argument_defaults) :] if len(argument_defaults) else []

        for kwarg in keyword_arguments:
            kwarg_type_hint = argument_type_hints.get(kwarg)
            if kwarg in kwargs or kwarg_type_hint is None or not context.exists(kwarg_type_hint):
                # if the keyword argument was specified in this specific call to `original_function`
                # or
                # if there is no type hint for the keyword argument
                # or
                # if ApplicationContext doesn't have an implementation for the keyword argument
                # then
                # don't inject
                continue

            kwargs[kwarg] = context.implementation(kwarg_type_hint)

        return original_function(*args, **kwargs)

    return wrapper


@singleton
class ApplicationContext:
    def __init__(self):
        self._implementation_map: dict[type[Any], Any] = {}

    def register[T](self, identifier: type[T], implementation: T):
        self._implementation_map[identifier] = implementation

    def exists(self, identifier: type[Any]) -> bool:
        return identifier in self._implementation_map

    def implementation[T](self, identifier: type[T]) -> T:
        return self._implementation_map[identifier]

    def reset(self):
        self._implementation_map.clear()
