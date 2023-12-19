import time
import sys
from queue import PriorityQueue
import tkinter as tk
import customtkinter
from typing import Dict
from pyamaze import maze, COLOR, agent, textLabel

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class Maze:
    def __init__(self, size=(10, 10), loopPercent=100):
        self.maze_size = size
        self.loop = loopPercent
        self.m = None

    def reset(self) -> None: 
        self.m = maze(self.maze_size[0], self.maze_size[1])
        self.m.CreateMaze(loopPercent=self.loop, theme=COLOR.dark)

    def dfs(self) -> Dict:
        start = (self.m.rows, self.m.cols)
        goal = (1, 1)
        explored = set()
        explored.add(start)
        frontier = [start]
        pathdfs = {}

        while frontier:
            currCell = frontier.pop()

            for d in 'ESWN':
                if self.m.maze_map[currCell][d]:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])

                    if childCell in explored: continue

                    explored.add(childCell)
                    frontier.append(childCell)
                    pathdfs[childCell] = currCell

        fwdPath = {}
        cell = goal

        while cell != start:
            try:
                fwdPath[pathdfs[cell]] = cell
                cell = pathdfs[cell]
            except:
                print("Path Not Found!")
                return

        return fwdPath

    def bfs(self) -> Dict: 
        start = (self.m.rows, self.m.cols)
        goal = (1, 1)
        explored = set()
        explored.add(start)
        frontier = [start]
        pathbfs = {}

        while frontier:
            currCell = frontier.pop(0)

            for d in 'ESNW':
                if self.m.maze_map[currCell][d]:
                    if d == 'E':
                        childCell = (currCell[0], currCell[1] + 1)
                    elif d == 'W':
                        childCell = (currCell[0], currCell[1] - 1)
                    elif d == 'N':
                        childCell = (currCell[0] - 1, currCell[1])
                    elif d == 'S':
                        childCell = (currCell[0] + 1, currCell[1])

                    if childCell in explored: continue

                    explored.add(childCell)
                    frontier.append(childCell)
                    pathbfs[childCell] = currCell

        fwdPath = {}
        cell = goal

        while cell != start:
            try:
                fwdPath[pathbfs[cell]] = cell
                cell = pathbfs[cell]
            except:
                print("Path Not Found!", file=sys.stderr)
                return

        return fwdPath

    def aStar(self): 
        h = lambda cell1, cell2 : abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1]) 
        start = (self.m.rows, self.m.cols)
        goal = (1, 1)
        g_score = {cell : float('inf') for cell in self.m.grid}
        g_score[start] = 0
        f_score = {cell : float('inf') for cell in self.m.grid}
        f_score[start] = h(start, goal)
        open = PriorityQueue()
        open.put((h(start, goal), h(start, goal), start))
        aPath = {}
        while not open.empty():
            curCell = open.get()[2]
            if curCell == goal: break
            for d in 'EWSN':
                if self.m.maze_map[curCell][d] == True:
                    if d == 'E':
                        childCell = (curCell[0], curCell[1] + 1)
                    elif d == 'W':
                        childCell = (curCell[0], curCell[1] - 1)
                    elif d == 'N':
                        childCell = (curCell[0] - 1, curCell[1])
                    elif d == 'S':
                        childCell = (curCell[0] + 1, curCell[1])
                    temp_g_score = g_score[curCell] + 1
                    temp_f_score = temp_g_score + h(childCell, goal)
                    if temp_f_score < f_score[childCell]:
                        g_score[childCell] = temp_g_score
                        f_score[childCell] = temp_f_score
                        open.put((temp_f_score, h(childCell, goal), childCell))
                        aPath[childCell] = curCell
        
        fwdPath = {}
        cell = goal
        while cell != start:
            try:
                fwdPath[aPath[cell]] = cell
                cell = aPath[cell]
            except:
                print("Path Not Found!", file=sys.stderr)
                return
        
        return fwdPath

    def dijkstra(self): ...
    def gbf(self): ...
    def bellman(self): ...
    def prim(self): ...
    def krushal(self): ...

    def show(self, algo_names, agent_color=COLOR.green, _filled=True, _footprint=True):
        path = []
        elapsed_times = []
        colors = [COLOR.red, COLOR.cyan, COLOR.yellow, COLOR.green, COLOR.blue]

        for algo_name in algo_names:
            if algo_name == 'DFS':
                start = time.time()
                path.append(self.dfs())
                end = time.time()
                elapsed_times.append('{:f}s'.format(float(end-start)))
            elif algo_name == 'BFS':
                start = time.time()
                path.append(self.bfs())
                end = time.time()
                elapsed_times.append('{:f}s'.format(float(end-start)))
            elif algo_name == 'aStar':
                start = time.time()
                path.append(self.aStar())
                end = time.time()
                elapsed_times.append('{:f}s'.format(float(end-start)))

        if self.m:
            res = ''
            for i in range(len(algo_names)):
                res += f'{algo_names[i]}({elapsed_times[i]}) Path Cost : {len(path[i])} | '
            
            textLabel(self.m, res + 'Path Found ', True)

            for i in range(len(algo_names)):
                a = agent(self.m, filled=_filled, footprints=_footprint, color=colors[i%5])
                self.m.tracePath({a : path[i]})
        else: 
            print("Maze not Declared!", file=sys.stderr)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #--- MAZE ---
        self.m_size = (10, 10)
        self.mazeObject : Maze = Maze(size=self.m_size)
        self.algo_name : str = None
        self.path : Dict = None
        self._filled = True
        self._footprints = True
        self._algo = {'DFS' : True, 'BFS' : False, 'aStar' : False, 'Dijsktra' : False, 'Bellman' : False, 'Prim' : False, 'Krushkal' : False}

        #--- Window ---
        self.title("Maze GUI")
        self.geometry(f"{1100}x{580}")

        #--- Grid Layout(4x4) ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #--- Sidebar and Widgets ---
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.other_sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.other_sidebar_frame.grid(row=0, column=4, rowspan=4, sticky='nsew')

        self.textbox = customtkinter.CTkTextbox(self, width=250, height=500)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.other_sidebar_frame, label_text="Select Algorithms", label_font=customtkinter.CTkFont(size=20, weight='bold'))
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []

        self.other_scrollable_frame = customtkinter.CTkScrollableFrame(self.other_sidebar_frame, label_text="Customize Maze", label_font=customtkinter.CTkFont(size=20, weight='bold'))
        self.other_scrollable_frame.grid(row=2, column=2, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.other_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.other_scrollable_frame_switches = []

        self.main_button = customtkinter.CTkButton(master=self.other_sidebar_frame, border_width=2, text='Generate Maze', text_color=("gray10", "#DCE4EE"), command=self.run)
        self.main_button.grid(row=3, column=2, padx=(15, 15), pady=(15, 15), sticky="nsew")

        self.slider_1 = customtkinter.CTkSlider(self.other_scrollable_frame, from_=5, to=50, number_of_steps=11, command=self.change_maze_size)
        self.slider_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.other_scrollable_frame_switches.append(self.slider_1)

        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.other_scrollable_frame, text='Filled', command=self.change_filled)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="w")

        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.other_scrollable_frame, text='Footprints', command=self.change_footprints)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="w")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Maze GUI", text_color='yellow', font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_checkbox_1 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='DFS', command=self.select_dfs)
        self.sidebar_checkbox_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_checkbox_2 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='BFS', command=self.select_bfs)
        self.sidebar_checkbox_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_checkbox_3 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='A*', command=self.select_aStar)
        self.sidebar_checkbox_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_checkbox_4 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='Dijstra', command=self.select_dij)
        self.sidebar_checkbox_4.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_checkbox_5 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='GBF', command=self.select_gbf)
        self.sidebar_checkbox_5.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_checkbox_6 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='Bellman', command=self.select_bell)
        self.sidebar_checkbox_6.grid(row=6, column=0, padx=20, pady=10)

        self.sidebar_checkbox_7 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='Prim', command=self.select_prim)
        self.sidebar_checkbox_7.grid(row=7, column=0, padx=20, pady=10)

        self.sidebar_checkbox_8 = customtkinter.CTkCheckBox(master=self.scrollable_frame, text='Kruskal', command=self.select_krush)
        self.sidebar_checkbox_8.grid(row=8, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        #--- Default Values ---
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.checkbox_1.select()
        self.checkbox_2.select()
        self.sidebar_checkbox_1.select()
        self.sidebar_checkbox_4.configure(state='disabled')
        self.sidebar_checkbox_5.configure(state='disabled')
        self.sidebar_checkbox_6.configure(state='disabled')
        self.sidebar_checkbox_7.configure(state='disabled')
        self.sidebar_checkbox_8.configure(state='disabled')

    def change_maze_size(self, new_size: int):
        new_size = int(new_size/5) * 5
        if new_size != self.m_size[0]:
            self.textbox.insert('0.0', f">>>Size ({self.m_size[0]}, {self.m_size[1]}) --> ({new_size}, {new_size})\n")
            self.m_size = (new_size, new_size)
            self.mazeObject.maze_size = self.m_size

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def select_dfs(self):
        algo_name = 'DFS'
        if self._algo[algo_name]: 
            self._algo[algo_name] = False
            self.textbox.insert('0.0', f'>>>(Algorithm) {algo_name} -> Removed\n')
        else: 
            self._algo[algo_name] = True
            self.textbox.insert('0.0', f'>>>(Algorithm) {algo_name} -> Selected\n')
    
    def select_bfs(self):
        algo_name = 'BFS'
        if self._algo[algo_name]: 
            self._algo[algo_name] = False
            self.textbox.insert('0.0', f'>>>(Algorithm) {algo_name} -> Removed\n')
        else: 
            self._algo[algo_name] = True
            self.textbox.insert('0.0', f'>>>(Algorithm) {algo_name} -> Selected\n')
    
    def select_aStar(self):
        algo_name = 'aStar'
        if self._algo[algo_name]: 
            self._algo[algo_name] = False
            self.textbox.insert('0.0', f'>>>(Algorithm) A* -> Removed\n')
        else: 
            self._algo[algo_name] = True
            self.textbox.insert('0.0', f'>>>(Algorithm) A* -> Selected\n')

    def select_dij(self): ...
    def select_gbf(self): ...
    def select_bell(self): ...
    def select_prim(self): ...
    def select_krush(self): ...

    def change_filled(self):
        self._filled = False if self._filled else True
        self.textbox.insert('0.0', f'>>>(Filled) attribute set to {self._filled}\n')

    def change_footprints(self):
        self._footprints = False if self._footprints else True
        self.textbox.insert('0.0', f'>>>(Footprints) attribute set to {self._footprints}\n')

    def run(self): 
        algo_names = []
        if self._algo['DFS'] : algo_names.append('DFS') 
        if self._algo['BFS'] : algo_names.append('BFS')
        if self._algo['aStar'] : algo_names.append('aStar')
        if self._algo['Dijsktra'] : algo_names.append('Dijsktra')
        if self._algo['Bellman'] : algo_names.append('Bellman')
        if self._algo['Prim'] : algo_names.append('Prim')
        if self._algo['Krushkal'] : algo_names.append('Krushkal')

        if not len(algo_names):
            self.textbox.insert('0.0', '>>>(Error) No Algorithm Selected!\n')
            return

        self.textbox.insert('0.0', 'Generating Maze ...')
        self.destroy()
        self.mazeObject.reset()

        self.mazeObject.show(algo_names)

if __name__ == '__main__':
    app = App()
    app.mainloop() 