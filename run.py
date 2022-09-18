import inspect

import flake8
import black
print(flake8.__file__)
print(black.__file__)
A = inspect.getfile(flake8)
print(A)