

"""
decorator.py
Description: How decorators work.
Decorators are functions that accept a function as input and then return a new function

"""


from datetime import datetime
import time


def notify_proto(f):
    """ A prototype decorator to notify user
    when a function is enterred and exited."""
    def wrapper():
        print("Enter: ", f.__name__)
        f()
        print("Exit : ", f.__name__)

    return wrapper


def notify(f):
    """ A correct decorator to notify user
    when a function is enterred and exited."""
    def wrapper(*args, **kwargs):
        print("Enter: ", f.__name__)
        rslt = f(*args, **kwargs)
        print("Exit : ", f.__name__)
        return rslt

    return wrapper

def do_twice(f):
    def wrapper(*args, **kwargs):
        z = f(*args, **kwargs)
        f(*args, **kwargs)
        return z

    return wrapper


def log(f):
    """ A correct decorator to notify user
    when a function is enterred and exited."""
    def wrapper(*args, **kwargs):
        print(str(datetime.now()) + ": Entering: ", f.__name__)
        return f(*args, **kwargs)

    return wrapper


def timer(f):
    """ Modify a function so that it now reports the elapsed time """
    def wrapper(*args, **kwargs):
        start = time.time()
        val = f(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print("Elapsed time: ", elapsed)
        return val

    return wrapper



def hello_world():
    print("Hello World!")


@do_twice
@notify
def hello(name="World"):
    """ say hello to <name> """
    print("Hello", name)

@timer
def myfunc(x):
    return 3*x + 1

@timer
def squares(n):
    return [i**2 for i in range(n)]





def main():



    z = myfunc(10)
    print(z)


    squares(100000000)

if __name__ == '__main__':
    main()

