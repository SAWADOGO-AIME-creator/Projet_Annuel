"""
Module: algorithms.py
Description: Implémentation des algorithmes de théorie des graphes
             pour génération et résolution de labyrinthes

Algorithmes implémentés :
  - DFS (Depth-First Search) : O(V+E) - Génération
  - Kruskal : O(E log E) - Génération avec Union-Find
  - Prim : O(V²) - Génération (variante greedy)
  - BFS : O(V+E) - Résolution optimale
  - Dijkstra : O(V²) ou O((V+E) log V) - Résolution avec poids

Références: Introduction to Algorithms (Cormen, Leiserson, Rivest, Stein)
"""

import random
from collections import deque
from typing import List, Optional, Set, Dict, Tuple
from .graph import Graph


class UnionFind:
    """
    Structure Union-Find pour l'algorithme de Kruskal.
    
    Complexité amortie :
    - Initialisation: O(n)
    - Find: O(α(n)) avec compression de chemin
    - Union: O(α(n)) avec union par rang
    où α(n) est la fonction inverse d'Ackermann (α(n) ≤ 4 en pratique)
    """
    
    def __init__(self, n: int):
        """Initialise la structure Union-Find."""
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x: int) -> int:
        """
        Trouve le représentant de x (compression de chemin).
        
        Complexité: O(α(n))
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compression
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """
        Unifie les ensembles contenant x et y (union par rang).
        Retourne True si l'union a été effectuée.
        
        Complexité: O(α(n))
        """
        px, py = self.find(x), self.find(y)
        
        if px == py:
            return False
        
        # Union par rang
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True


class Algorithms:
    """Classe statique contenant les algorithmes de graphes."""
    
    # ========== ALGORITHMES DE GÉNÉRATION ==========
    
    @staticmethod
    def dfs_maze_generation(graph: Graph, width: int, height: int, start: int = 0) -> Graph:
        """
        Génère un labyrinthe parfait via DFS aléatoire (Backtracking).
        
        Principe :
          1. On démarre d'une cellule
          2. On visite un voisin non visité aléatoirement
          3. On ajoute une arête
          4. On continue récursivement
        
        Garantit un arbre couvrant (pas de cycles).
        
        Complexité: O(V + E) = O(width × height)
        
        Args:
            graph: Graphe initial (grille complète)
            width: Largeur du labyrinthe
            height: Hauteur du labyrinthe
            start: Sommet de départ
        
        Returns:
            Graph: Labyrinthe généré (arbre couvrant)
        """
        visited = set()
        result = Graph()
        
        # Initialiser les sommets
        for i in range(width * height):
            result.add_vertex(i)
        
        def dfs_helper(current: int):
            visited.add(current)
            
            # Voisins possibles (droite, bas, gauche, haut)
            neighbors = []
            x, y = current % width, current // width
            
            # Droite
            if x < width - 1:
                neighbors.append(current + 1)
            # Bas
            if y < height - 1:
                neighbors.append(current + width)
            # Gauche
            if x > 0:
                neighbors.append(current - 1)
            # Haut
            if y > 0:
                neighbors.append(current - width)
            
            # Mélanger et visiter
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if neighbor not in visited:
                    result.add_edge(current, neighbor)
                    dfs_helper(neighbor)
        
        dfs_helper(start)
        return result
    
    @staticmethod
    def kruskal_maze_generation(graph: Graph, width: int, height: int) -> Graph:
        """
        Génère un labyrinthe parfait via l'algorithme de Kruskal.
        
        Principe :
          1. Créer une grille complète d'arêtes
          2. Mélanger aléatoirement les arêtes
          3. Pour chaque arête, l'ajouter si elle ne crée pas de cycle
          4. Utiliser Union-Find pour détecter les cycles
        
        Garantit un arbre couvrant minimal.
        
        Complexité: O(E log E) = O(V log V)
        
        Args:
            graph: Graphe (ignoré, on construit depuis zéro)
            width: Largeur
            height: Hauteur
        
        Returns:
            Graph: Labyrinthe généré
        """
        result = Graph()
        
        # Initialiser les sommets
        for i in range(width * height):
            result.add_vertex(i)
        
        # Créer toutes les arêtes possibles
        edges = []
        for y in range(height):
            for x in range(width):
                cell = y * width + x
                if x < width - 1:  # Arête vers la droite
                    edges.append((cell, cell + 1))
                if y < height - 1:  # Arête vers le bas
                    edges.append((cell, cell + width))
        
        # Mélanger les arêtes
        random.shuffle(edges)
        
        # Union-Find
        uf = UnionFind(width * height)
        
        # Ajouter les arêtes
        for u, v in edges:
            if uf.union(u, v):
                result.add_edge(u, v)
        
        return result
    
    @staticmethod
    def prim_maze_generation(graph: Graph, width: int, height: int, start: int = 0) -> Graph:
        """
        Génère un labyrinthe parfait via l'algorithme de Prim.
        
        Principe :
          1. Commencer avec un seul sommet
          2. Ajouter aléatoirement un sommet adjacent
          3. Répéter jusqu'à avoir tous les sommets
        
        Complexité: O(V²)
        
        Args:
            graph: Graphe
            width: Largeur
            height: Hauteur
            start: Sommet de départ
        
        Returns:
            Graph: Labyrinthe généré
        """
        result = Graph()
        visited = set()
        
        # Initialiser les sommets
        for i in range(width * height):
            result.add_vertex(i)
        
        visited.add(start)
        frontier = []  # Arêtes vers des sommets non visités
        
        # Ajouter les arêtes initiales
        x, y = start % width, start // width
        neighbors = []
        if x < width - 1:
            neighbors.append(start + 1)
        if y < height - 1:
            neighbors.append(start + width)
        if x > 0:
            neighbors.append(start - 1)
        if y > 0:
            neighbors.append(start - width)
        
        for neighbor in neighbors:
            if neighbor not in visited:
                frontier.append((start, neighbor))
        
        # Construire l'arbre
        while frontier:
            # Choisir une arête aléatoire
            idx = random.randint(0, len(frontier) - 1)
            u, v = frontier.pop(idx)
            
            if v not in visited:
                visited.add(v)
                result.add_edge(u, v)
                
                # Ajouter nouvelles arêtes
                x, y = v % width, v // width
                neighbors = []
                if x < width - 1:
                    neighbors.append(v + 1)
                if y < height - 1:
                    neighbors.append(v + width)
                if x > 0:
                    neighbors.append(v - 1)
                if y > 0:
                    neighbors.append(v - width)
                
                for neighbor in neighbors:
                    if neighbor not in visited:
                        frontier.append((v, neighbor))
        
        return result
    
    # ========== ALGORITHMES DE RÉSOLUTION ==========
    
    @staticmethod
    def bfs_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
        """
        Trouve le chemin le plus court via BFS.
        
        Principe :
          1. Parcourir le graphe en largeur d'abord
          2. Tracker les parents pour reconstruire le chemin
        
        Complexité: O(V + E)
        Optimalité: OUI - Trouve le chemin le plus court
        
        Args:
            graph: Graphe
            start: Sommet de départ
            end: Sommet cible
        
        Returns:
            list: Chemin de start à end, ou None
        """
        if start == end:
            return [start]
        
        visited = {start}
        parent = {start: None}
        queue = deque([start])
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                # Reconstruire le chemin
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))
            
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return None
    
    @staticmethod
    def dijkstra_shortest_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
        """
        Trouve le chemin le plus court via Dijkstra.
        
        Principe :
          1. Initialiser distances à ∞
          2. Choisir le sommet non visité avec la plus petite distance
          3. Mettre à jour les distances des voisins
          4. Répéter jusqu'au sommet cible
        
        Complexité: O(V²) avec tableau, O((V+E) log V) avec heap
        Optimalité: OUI pour poids positifs
        
        Args:
            graph: Graphe
            start: Sommet de départ
            end: Sommet cible
        
        Returns:
            list: Chemin de start à end, ou None
        """
        distances = {v: float('inf') for v in range(graph.get_num_vertices())}
        distances[start] = 0
        parent = {v: None for v in range(graph.get_num_vertices())}
        unvisited = set(range(graph.get_num_vertices()))
        
        while unvisited:
            # Trouver le sommet non visité avec la plus petite distance
            current = min(unvisited, key=lambda v: distances[v])
            
            if distances[current] == float('inf'):
                break  # Pas de chemin
            
            if current == end:
                # Reconstruire le chemin
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))
            
            unvisited.remove(current)
            
            # Mettre à jour les distances
            for neighbor in graph.get_neighbors(current):
                if neighbor in unvisited:
                    new_dist = distances[current] + 1
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        parent[neighbor] = current
        
        return None
    
    @staticmethod
    def dfs_any_path(graph: Graph, start: int, end: int) -> Optional[List[int]]:
        """
        Trouve n'importe quel chemin via DFS (pas forcément le plus court).
        
        Complexité: O(V + E)
        Optimalité: NON
        
        Args:
            graph: Graphe
            start: Sommet de départ
            end: Sommet cible
        
        Returns:
            list: Un chemin de start à end, ou None
        """
        visited = set()
        
        def dfs(current, target, path):
            if current == target:
                return path + [current]
            
            visited.add(current)
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    result = dfs(neighbor, target, path + [current])
                    if result:
                        return result
            
            return None
        
        return dfs(start, end, [])
    
    # ========== ALGORITHMES AVEC ÉTAPES (POUR ANIMATION) ==========
    
    @staticmethod
    def bfs_with_steps(graph: Graph, start: int, end: int) -> Tuple[Optional[List[int]], List[int]]:
        """
        BFS retournant le chemin ET l'ordre d'exploration.
        Utile pour animation.
        
        Returns:
            tuple: (chemin_solution, ordre_exploration)
        """
        if start == end:
            return [start], [start]
        
        visited = {start}
        parent = {start: None}
        queue = deque([start])
        visited_order = [start]
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path)), visited_order
            
            for neighbor in sorted(graph.get_neighbors(current)):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)
                    visited_order.append(neighbor)
        
        return None, visited_order
    
    @staticmethod
    def dijkstra_with_steps(graph: Graph, start: int, end: int) -> Tuple[Optional[List[int]], List[int]]:
        """
        Dijkstra retournant le chemin ET l'ordre de traitement.
        Utile pour animation.
        
        Returns:
            tuple: (chemin_solution, ordre_traitement)
        """
        distances = {v: float('inf') for v in range(graph.get_num_vertices())}
        distances[start] = 0
        parent = {v: None for v in range(graph.get_num_vertices())}
        unvisited = set(range(graph.get_num_vertices()))
        visited_order = []
        
        while unvisited:
            current = min(unvisited, key=lambda v: distances[v])
            
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            visited_order.append(current)
            
            if current == end:
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path)), visited_order
            
            for neighbor in graph.get_neighbors(current):
                if neighbor in unvisited:
                    new_dist = distances[current] + 1
                    if new_dist < distances[neighbor]:
                        distances[neighbor] = new_dist
                        parent[neighbor] = current
        
        return None, visited_order
