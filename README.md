# Snowcrystal Formation with Hexagonal Cellular Automata

In this project we use a custom grid from hexagonal cellular automate to simulate the formation of snow crystals through diffusion limited aggregation. The goal is to research which underlying conditions the different archetypes of formations depend on.

![](snow-crystal.gif)

## Getting Started

First make sure you have a version of Python 3 and all the prerequisite packages (see below) installed.

Our code offer 3 ways of viewing the formation of a snow crystal: A real time animation of the crystal lattice in the simulation over time, a final drawing at the end of the simulation and a series of experiments with optional drawing.

To choose which of the 3 ways you'd like to execute, run the main.py file in your terminal with:
```
python main.py
```
You will then be prompted to enter which way you'd like to execute. 
The options are:
- animate / 1
- draw / 2
- experiment / 3

The code will execute by entering one of these 3 strings/numbers.

### Prerequisites

In this project we strictly use Python 3. All packages needed can be downloaded with pip or conda install.

```
pip install pyglet
pip install pillow
pip install numpy
pip install pandas
```

## Authors
- **Fenna Houtsma**
- **Christopher Buch Madsen**
- **Guido Vaessen** 

## Acknowledgments

This project was part of the Project Computational Science course in the Computational Science minor at the Universtiy of Amsterdam.
