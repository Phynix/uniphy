# uniphy
Uniphy stands for "**Uni**versity **Phy**sics". The package focuses on specialised functionality for research and teaching on university level.

## First Project
The first project just started is the package called **uniphy.units**. It's goal is to create a possiblity to conveniently handle physical units in python.
The core class will be called **Unit** with the following attributes and features:
  * Name: A unit has a name like "J" or "Angstroem".
  * Description: An optional description.
  * Dimension: The dimension in lenght, mass, etc.
  * Value: The value of the unit.
  * Transaltion Factor: Factor to translate into SI units.
  * Forbidden operations like addition of units with differing dimension.
  * A subclass RangedUnit with max and min values.

A first demo is hoped to be released next summer.
