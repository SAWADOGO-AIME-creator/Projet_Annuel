#!/usr/bin/env python3
"""
Module: gui.py
Description: Interface graphique Tkinter pour interaction avec le labyrinthe

Fonctionnalités :
  - Génération interactive (choisir taille, algorithme)
  - Animation de la résolution (étape par étape)
  - Contrôle de vitesse
  - Affichage des statistiques
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
from typing import List, Optional

# Ajouter le chemin pour imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.labyrinth import Labyrinth


class LabyrinthGUI:
    """Interface graphique pour labyrinthe."""
    
    def __init__(self, root):
        """Initialise la fenêtre."""
        self.root = root
        self.root.title("🧩 Générateur et Résolveur de Labyrinthes")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.labyrinth: Optional[Labyrinth] = None
        self.canvas: Optional[tk.Canvas] = None
        self.cell_size = 25
        self.animation_steps: List[int] = []
        self.solution_path: Optional[List[int]] = None
        self.is_animating = False
        self.animation_delay = 50
        
        # Couleurs
        self.COLORS = {
            'passage': '#FFFFFF',
            'wall': '#000000',
            'start': '#00CC00',
            'end': '#FF0000',
            'visited': '#FFB6C1',
            'path': '#0066FF',
        }
        
        self.setup_ui()
        self.generate_new()
    
    def setup_ui(self):
        """Configure l'interface utilisateur."""
        # === CONTRÔLES ===
        control_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Dimensions
        dim_frame = ttk.Frame(control_frame)
        dim_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dim_frame, text="Largeur:").pack(side=tk.LEFT, padx=5)
        self.width_var = tk.IntVar(value=12)
        ttk.Spinbox(dim_frame, from_=5, to=25, textvariable=self.width_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dim_frame, text="Hauteur:").pack(side=tk.LEFT, padx=5)
        self.height_var = tk.IntVar(value=12)
        ttk.Spinbox(dim_frame, from_=5, to=25, textvariable=self.height_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Algorithmes
        algo_frame = ttk.Frame(control_frame)
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="Génération:").pack(side=tk.LEFT, padx=5)
        self.gen_algo = tk.StringVar(value="DFS")
        ttk.Combobox(algo_frame, textvariable=self.gen_algo, values=["DFS", "Kruskal", "Prim"], state="readonly", width=12).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(algo_frame, text="Résolution:").pack(side=tk.LEFT, padx=5)
        self.solve_algo = tk.StringVar(value="BFS")
        ttk.Combobox(algo_frame, textvariable=self.solve_algo, values=["BFS", "Dijkstra", "DFS"], state="readonly", width=12).pack(side=tk.LEFT, padx=5)
        
        # Boutons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="🔄 Générer", command=self.generate_new).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="▶️ Résoudre", command=self.solve).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="⏸️ Pause", command=self.pause).pack(side=tk.LEFT, padx=5)
        
        # Vitesse
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Vitesse:").pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.IntVar(value=50)
        ttk.Scale(speed_frame, from_=10, to=200, orient=tk.HORIZONTAL, variable=self.speed_var, command=self.update_speed).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.speed_label = ttk.Label(speed_frame, text="50ms")
        self.speed_label.pack(side=tk.LEFT, padx=5)
        
        # === CANVAS ===
        canvas_frame = ttk.LabelFrame(self.root, text="Labyrinthe", padding=5)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        
        # === INFO ===
        info_frame = ttk.LabelFrame(self.root, text="Information", padding=5)
        info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.info_label = ttk.Label(info_frame, text="", foreground='#333333')
        self.info_label.pack(fill=tk.X)
        
        # Legend
        legend_text = ("Légende : "
                      "🟩=Passage (blanc), 🟫=Mur (noir), 🟢=Départ (vert), "
                      "🔴=Sortie (rouge), 🟥=Exploré (rose), 🟦=Chemin (bleu)")
        ttk.Label(self.root, text=legend_text, foreground='#666666', wraplength=1000).pack(padx=10, pady=(0, 5))
    
    def update_speed(self, value):
        """Met à jour la vitesse."""
        self.animation_delay = 200 - int(float(value))
        self.speed_label.config(text=f"{self.animation_delay}ms")
    
    def generate_new(self):
        """Génère un nouveau labyrinthe."""
        try:
            width = self.width_var.get()
            height = self.height_var.get()
            algo = self.gen_algo.get()
            
            self.labyrinth = Labyrinth(width, height)
            if algo == "DFS":
                self.labyrinth.generate_dfs()
            elif algo == "Kruskal":
                self.labyrinth.generate_kruskal()
            else:
                self.labyrinth.generate_prim()
            
            self.solution_path = None
            self.animation_steps = []
            self.draw_labyrinth()
            self.update_info()
        except Exception as e:
            self.info_label.config(text=f"Erreur: {e}", foreground='red')
    
    def solve(self):
        """Résout le labyrinthe."""
        if not self.labyrinth or self.is_animating:
            return
        
        self.is_animating = True
        algo = self.solve_algo.get()
        
        try:
            if algo == "BFS":
                solution, steps = self.labyrinth.solve_bfs_with_animation()
            elif algo == "Dijkstra":
                solution, steps = self.labyrinth.solve_dijkstra_with_animation()
            else:
                self.labyrinth.solve_dfs()
                solution = self.labyrinth.get_solution()
                steps = []
            
            self.solution_path = solution
            self.animation_steps = steps if steps else []
            
            # Animer
            self.animate_exploration(0)
        except Exception as e:
            self.info_label.config(text=f"Erreur: {e}", foreground='red')
            self.is_animating = False
    
    def animate_exploration(self, step: int):
        """Anime l'exploration."""
        if not self.is_animating or step >= len(self.animation_steps):
            if self.is_animating and self.solution_path:
                self.animate_solution(0)
            return
        
        visited = self.animation_steps[:step + 1]
        self.draw_labyrinth(visited=visited)
        
        self.root.after(self.animation_delay, lambda: self.animate_exploration(step + 1))
    
    def animate_solution(self, step: int):
        """Anime le tracé de la solution."""
        if not self.is_animating or not self.solution_path or step >= len(self.solution_path):
            self.is_animating = False
            self.update_info()
            return
        
        path = self.solution_path[:step + 1]
        visited = set(self.animation_steps)
        self.draw_labyrinth(visited=visited, path=path)
        
        self.root.after(self.animation_delay, lambda: self.animate_solution(step + 1))
    
    def draw_labyrinth(self, visited: Optional[List[int]] = None, path: Optional[List[int]] = None):
        """Dessine le labyrinthe."""
        if not self.labyrinth:
            return
        
        self.canvas.delete('all')
        
        w = self.labyrinth.width
        h = self.labyrinth.height
        g = self.labyrinth.graph
        
        visited_set = set(visited) if visited else set()
        path_set = set(path) if path else set()
        
        # Cellules
        for cell in range(w * h):
            x, y = cell % w, cell // w
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            
            if cell == self.labyrinth.start:
                color = self.COLORS['start']
            elif cell == self.labyrinth.end:
                color = self.COLORS['end']
            elif cell in path_set:
                color = self.COLORS['path']
            elif cell in visited_set:
                color = self.COLORS['visited']
            else:
                color = self.COLORS['passage']
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#DDD')
        
        # Murs
        for cell in range(w * h):
            x, y = cell % w, cell // w
            x1, y1 = x * self.cell_size, y * self.cell_size
            x2, y2 = x1 + self.cell_size, y1 + self.cell_size
            
            if x < w - 1 and not g.has_edge(cell, cell + 1):
                self.canvas.create_line(x2, y1, x2, y2, fill=self.COLORS['wall'], width=2)
            
            if y < h - 1 and not g.has_edge(cell, cell + w):
                self.canvas.create_line(x1, y2, x2, y2, fill=self.COLORS['wall'], width=2)
        
        self.canvas.update()
    
    def on_canvas_click(self, event):
        """Gère les clics sur le canvas."""
        if not self.labyrinth:
            return
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        cell = y * self.labyrinth.width + x
        if cell == self.labyrinth.start:
            self.solve()
    
    def pause(self):
        """Pause l'animation."""
        self.is_animating = False
    
    def update_info(self):
        """Affiche les infos."""
        if not self.labyrinth:
            return
        info = self.labyrinth.get_info()
        text = (f"Taille: {info['width']}×{info['height']} | "
                f"Génération: {info['generation_algorithm']} | "
                f"Arêtes: {info['num_edges']} | "
                f"Résolution: {info['solution_algorithm']} | "
                f"Chemin: {info['solution_length'] if info['solution_length'] else '—'} cases")
        self.info_label.config(text=text, foreground='#333333')


def run_gui():
    """Lance la GUI."""
    root = tk.Tk()
    app = LabyrinthGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
