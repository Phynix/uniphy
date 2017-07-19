[![PyPI version](https://badge.fury.io/py/uniphy.svg)](https://badge.fury.io/py/uniphy)
[![Build Status](https://travis-ci.org/Phynix/uniphy.svg?branch=master)](https://travis-ci.org/Phynix/uniphy)
[![Code Health](https://landscape.io/github/Phynix/uniphy/master/landscape.svg?style=flat)](https://landscape.io/github/Phynix/uniphy/master)
[![Dependency Status](https://www.versioneye.com/user/projects/5967cb390fb24f004276ac8c/badge.svg?style=flat-square)](https://www.versioneye.com/user/projects/5967cb390fb24f004276ac8c)


# uniphy
Uniphy stands for "**Uni**versity **Phy**sics". The package focuses on specialised functionality for research and teaching on university level without a focus on a certain branch of physics or science. It is part of the Phynix project.

## Current projects

The package is still in its early stage of planning and first implemenations. It is currently not usable for any production-like application.


### Output

What if "print" would simply save everything also into a file if I want to and not if I don't want to? Or if only those "prints" will be saved which I want to be saved?

The answer is **Output** which does exactly the above (and more). But most of all, it does not change anything if not wanted.

Simply replace **every** print with out.print. And everything works as usual. One line will let you save the output. If you like. And won't if you don't.

Minimal example:

```python
import uniphy as up

out = up.output()
out.print("Same as print", "\nBut I can be saved as well.)

OR

out = up.output("/my/path/to/folder")
out.print("Same as print again, but will be saved this time")
```




### Units

The first project just started is the package called **uniphy.units**. It's goal is to create a possiblity to conveniently handle physical units in python.
The core class will be called **Unit** with the following attributes and features:
  * Name: A unit has a name like "J" or "Angstroem".
  * Description: An optional description.
  * Dimension: The dimension in lenght, mass, etc.
  * Value: The value of the unit.
  * Transaltion Factor: Factor to translate into SI units.
  * Forbidden operations like addition of units with differing dimension.
  * A subclass RangedUnit with max and min values.

Input and feedback is very welcome and can be posted as an issue. A first demo is hoped to be released next summer.