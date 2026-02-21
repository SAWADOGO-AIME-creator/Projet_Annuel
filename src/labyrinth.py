"""
Module: labyrinth.py
Description: Classe principale Labyrinth pour générer et résoudre des labyrinthes

Modélisation :
  Un labyrinthe est un graphe non-orienté connexe représentant :
  - Sommets (V) = cases / intersections
  - Arêtes (E) = couloirs / passages
  
  Propriétés garanties :
  - Connexité : il existe un chemin entre n'importe quel couple de cases
  - Arbre couvrant : V vertices, V-1 edges (pas de cycles)
"""

import random
from enum import Enum
from typing import List, Optional, Tuple
from .graph import Graph
from .algorithms import Algorithms


class LabyrinthType(Enum):
    """Types d'algorithmes de génération disponibles."""
    DFS = "DFS"
    KRUSKAL = "Kruskal"
    PRIM = "Prim"


class Labyrinth:
    """
    Classe représentant un labyrinthe comme un graphe non-orienté.
    
    Attributes:
        graph (Graph): Graphe sous-jacent
        width (int): Largeur du labyrinthe (en cases)
        height (int): Hauteur du labyrinthe (en cases)
        start (int): Sommet de départ (0 = coin haut-gauche)
        end (int): Sommet de sortie (width*height - 1 = coin bas-droit)
        generation_algorithm (str): Nom de l'algorithme utilisé
        solution_algorithm (str): Algorithme de résolution utilisé
        _solution (List[int]): Chemin solution trouvé
    """
    
    def __init__(self, width: int = 10, height: int = 10):
        """
        Initialise un labyrinthe vide.
        
        Args:
            width: Largeur en cases
            height: Hauteur en cases
        """
        self.width = width
        self.height = height
        self.graph = Graph()
        self.start = 0  # Coin haut-gauche
        self.end = width * height - 1  # Coin bas-droit
        
        # Initialiser les sommets
        for i in range(width * height):
            self.graph.add_vertex(i)
        
        self.generation_algorithm = None
        self.solution_algorithm = None
        self._solution: Optional[List[int]] = None
    
    def generate_dfs(self) -> None:
        """
        Génère un labyrinthe via DFS aléatoire.
        
        Complexité: O(width × height)
        """
        self.graph = Algorithms.dfs_maze_generation(self.graph, self.width, self.height)
        self.generation_algorithm = LabyrinthType.DFS.value
    
    def generate_kruskal(self) -> None:
        """
        Génère un labyrinthe via Kruskal.
        
        Complexité: O(V log V)
        """
        self.graph = Algorithms.kruskal_maze_generation(self.graph, self.width, self.height)
        self.generation_algorithm = LabyrinthType.KRUSKAL.value
    
    def generate_prim(self) -> None:
        """
        Génère un labyrinthe via Prim.
        
        Complexité: O(V²)
        """
        self.graph = Algorithms.prim_maze_generation(self.graph, self.width, self.height)
        self.generation_algorithm = LabyrinthType.PRIM.value
    
    def solve_bfs(self) -> Optional[List[int]]:
        """
        Résout le labyrinthe via BFS.
        
        Garantit le chemin le plus court.
        
        Complexité: O(V + E)
        
        Returns:
            list: Chemin ou None
        """
        self._solution = Algorithms.bfs_shortest_path(self.graph, self.start, self.end)
        self.solution_algorithm = "BFS"
        return self._solution
    
    def solve_bfs_with_animation(self) -> Tuple[Optional[List[int]], List[int]]:
        """
        Résout avec BFS et retourne aussi l'ordre d'exploration.
        Utile pour animation.
        
        Returns:
            tuple: (solution, explored_order)
        """
        solution, steps = Algorithms.bfs_with_steps(self.graph, self.start, self.end)
        self._solution = solution
        self.solution_algorithm = "BFS (animated)"
        return solution, steps
    
    def solve_dijkstra(self) -> Optional[List[int]]:
        """
        Résout le labyrinthe via Dijkstra.
        
        Complexité: O(V²) ou O((V+E) log V) avec heap
        
        Returns:
            list: Chemin ou None
        """
        self._solution = Algorithms.dijkstra_shortest_path(self.graph, self.start, self.end)
        self.solution_algorithm = "Dijkstra"
        return self._solution
    
    def solve_dijkstra_with_animation(self) -> Tuple[Optional[List[int]], List[int]]:
        """
        Résout avec Dijkstra et retourne aussi l'ordre de traitement.
        
        Returns:
            tuple: (solution, visited_order)
        """
        solution, steps = Algorithms.dijkstra_with_steps(self.graph, self.start, self.end)
        self._solution = solution
        self.solution_algorithm = "Dijkstra (animated)"
        return solution, steps
    
    def solve_dfs(self) -> Optional[List[int]]:
        """
        Résout le labyrinthe via DFS.
        
        Pas forcément optimal mais simple.
        
        Complexité: O(V + E)
        
        Returns:
            list: Chemin ou None
        """
        self._solution = Algorithms.dfs_any_path(self.graph, self.start, self.end)
        self.solution_algorithm = "DFS"
        return self._solution
    
    def get_solution(self) -> Optional[List[int]]:
        """Retourne la solution calculée précédemment."""
        return self._solution
    
    def get_solution_length(self) -> Optional[int]:
        """Retourne la longueur du chemin solution."""
        return len(self._solution) if self._solution else None
    
    def is_solution_valid(self, path: List[int]) -> bool:
        """
        Vérifie si un chemin est une solution valide.
        
        Args:
            path: Chemin à vérifier
        
        Returns:
            bool: True si valide
        """
        if not path or path[0] != self.start or path[-1] != self.end:
            return False
        
        for i in range(len(path) - 1):
            if not self.graph.has_edge(path[i], path[i + 1]):
                return False
        
        return True
    
    def get_info(self) -> dict:
        """Retourne les infos du labyrinthe."""
        return {
            'width': self.width,
            'height': self.height,
            'total_cells': self.width * self.height,
            'num_vertices': self.graph.get_num_vertices(),
            'num_edges': self.graph.get_num_edges(),
            'is_connected': self.graph.is_connected(),
            'generation_algorithm': self.generation_algorithm,
            'solution_algorithm': self.solution_algorithm,
            'solution_length': self.get_solution_length(),
        }
    
    def __repr__(self) -> str:
        """Représentation textuelle."""
        return (f"Labyrinth({self.width}x{self.height}, "
                f"edges={self.graph.get_num_edges()}, "
                f"algorithm={self.generation_algorithm})")
