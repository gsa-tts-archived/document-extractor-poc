import functools
import inspect
from typing import Any


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

        argument_specification = inspect.getfullargspec(original_function)
        argument_defaults = argument_specification.defaults or ()
        keyword_arguments = argument_specification.args[-len(argument_defaults) :] if len(argument_defaults) else []

        for kwarg in keyword_arguments:
            if kwarg in kwargs or not context.exists(kwarg):
                # if the keyword argument was specified in this specific call to `original_function`
                # or
                # if ApplicationContext doesn't have the keyword argument
                # then
                # don't inject
                continue

            kwargs[kwarg] = context.implementation(kwarg)

        return original_function(*args, **kwargs)

    return wrapper


@singleton
class ApplicationContext:
    def __init__(self):
        self._implementation_map: dict[str, Any] = {}

    def register(self, identifier: str, implementation: Any):
        self._implementation_map[identifier] = implementation

    def exists(self, identifier: str) -> bool:
        return identifier in self._implementation_map

    def implementation(self, identifier: str) -> Any:
        return self._implementation_map[identifier]
