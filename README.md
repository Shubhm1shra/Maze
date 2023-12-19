# Maze
Welcome to my Project 'Maze', an exciting project where I use the power of tkinter to demonstrate different path finding algorithms. 

- - - -

## Features 🔑
* __Tkinter__ : Utilize Tkinter(Custom Tkinter) Library for seamless and visually appealing User-Interface.
* __Pyamaze Integeration__ : Generate captivating mazes with Pyamaze library.
* __PathFinding Algorithms__ : Witness the efficiency of DFS, BFS and A* as agents utilizes them for maze traversal.

## Prerequisite 📚
Ensure that the following Libraries are installed on local system.
* Install Customtkinter : `python -m pip install customtkinter`
* Install Pyamaze : `python -m pip install pyamaze`

## Installation 📦
* Clone the repository using git clone command on local system.
* Run using : `python MAZE.py`

## How to Use 🤔
1. Clone the Repository
2. Once the application opens, select prefered Path-Finding Algorithms
3. Select prefered Agent options and Maze Size
4. Once Done, Click on 'Generate Maze'

## Note 📌
* __Currently Dijkstra and Bellman are not completed since both are Single Source Shortest Path Algorithms, Not the best choice for Maze Solving.__
* __Once 'Generate Maze' is clicked, the main application stops running since Pyamaze and tkinter utilize grid and pack functions offered by tkinter library which cannot be used at the same time, Hence one has to close for other to run.__
