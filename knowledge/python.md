# Python

## Decorators
A decorator is a function that takes another function and extends or modifies its behavior without changing the original function's source code.

A common pattern is:

def decorator(func):
    def wrapper(*args, **kwargs):
        # additional behavior
        return func(*args, **kwargs)
    return wrapper

Decorators are commonly used for logging, authentication, timing, caching, and validation.

## Generators
A generator is a Python function that uses the yield keyword to produce values lazily. Unlike a normal function that returns all results at once, a generator produces one value at a time.

Generators are useful when processing large datasets because they reduce memory consumption.

Example:
def numbers():
    for i in range(5):
        yield i

## List vs Tuple
A list is mutable, while a tuple is immutable. Lists are useful when elements need to change. Tuples are useful for fixed collections of values and can be used as dictionary keys when their elements are hashable.

## == vs is
The == operator compares values, while is checks whether two references point to the same object in memory.
