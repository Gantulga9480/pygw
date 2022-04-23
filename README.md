# **Simple Base class for implementing pygame application.**

# Install
    pip install git+https://github.com/Gantulga9480/Game.git#egg=Game

# Change Log

## 1.1.1:
- Added resolution constant to scalar class. Scalar values are rounded by default by const resolution (4).
- Added type check in plane property XY setter.
- Changed:
    ```
    plane.vector -> plane.createVector
    plane.rand_vector -> plane.createRandomVector
    ```
- Added vector length in pixel. property LENGTH.
- Added unit vector method. method unit.
- Updated plane arithmetic operator overloading.
- Updated vector arithmetic operator overloading.
- Added setter for length and direction properties.
- Hide pygame prompt.
- Added set_limit parameter to vector and plane.
- Vector limit changed min to max of space axes.

### 1.1.0:
- Added new module 'graphic'
- Added cartesian system in module 'graphic'. This module provides scalar, vector, plane abstractions for pygame projects.

### 1.0.1:
- Changed variable names.
- Added keys field.

### 1.0.0:
- Project published.