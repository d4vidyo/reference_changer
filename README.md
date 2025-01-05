# Description

This Python package allows you to copy a function or method and redirect specific references from one instance to another.

## Example

```python
from reference_changer import changeReference
def main():
    a = 0
    b = 1
    def f():
        print(a)
    f2 = changeReference(f, a, b)
    f()
    f2()
main()
```

Output:
```shell
0
1
```

# Installation

```shell
pip install git+https://github.com/d4vidyo/reference_changer.git@latest
```