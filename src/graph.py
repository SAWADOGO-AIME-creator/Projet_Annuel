"""
Module: graph.py
Description: Implémentation d'un graphe non-orienté pour modéliser un labyrinthe

Un labyrinthe est formalisé comme un graphe G = (V, E) où :
  - V : ensemble des sommets (cases/intersections)
  - E : ensemble des arêtes (couloirs/connexions)
  - Non orienté : si (u,v) ∈ E alors (v,u) ∈ E
"""

from collections import defaultdict
from typing import Set, Dict, List, Optional


class Graph:
    """
    Représentation d'un graphe non-orienté avec liste d'adjacence.
    
    Complexité :
    - add_vertex: O(1)
    - add_edge: O(1)
    - get_neighbors: O(1)
    - has_edge: O(1)
    - get_num_vertices: O(1)
    - get_num_edges: O(1)
    """
    
    def __init__(self):
        """Initialise un graphe vide."""
        self.adjacency_list: Dict[int, Set[int]] = defaultdict(set)
        self.num_vertices = 0
        self.num_edges = 0
    
    def add_vertex(self, vertex: int) -> None:
        """Ajoute un sommet au graphe."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = set()
            self.num_vertices += 1
    
    def add_edge(self, u: int, v: int) -> None:
        """
        Ajoute une arête entre u et v (non-orientée).
        
        Args:
            u: Premier sommet
            v: Deuxième sommet
        """
        # Assurer que les sommets existent
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Ajouter l'arête (non-orientée)
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
            self.num_edges += 1
    
    def remove_edge(self, u: int, v: int) -> None:
        """Supprime l'arête entre u et v."""
        if u in self.adjacency_list and v in self.adjacency_list[u]:
            self.adjacency_list[u].remove(v)
            self.adjacency_list[v].remove(u)
            self.num_edges -= 1
    
    def has_edge(self, u: int, v: int) -> bool:
        """Vérifie s'il existe une arête entre u et v."""
        return u in self.adjacency_list and v in self.adjacency_list[u]
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """Retourne les voisins d'un sommet."""
        return sorted(list(self.adjacency_list.get(vertex, [])))
    
    def get_num_vertices(self) -> int:
        """Retourne le nombre de sommets."""
        return self.num_vertices
    
    def get_num_edges(self) -> int:
        """Retourne le nombre d'arêtes."""
        return self.num_edges
    
    def is_connected(self) -> bool:
        """
        Vérifie si le graphe est connexe (via DFS).
        
        Complexité: O(V + E)
        """
        if self.num_vertices == 0:
            return True
        
        visited = set()
        stack = [0]
        
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                for neighbor in self.adjacency_list[v]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return len(visited) == self.num_vertices
    
    def get_all_edges(self) -> List[tuple]:
        """Retourne toutes les arêtes du graphe."""
        edges = []
        seen = set()
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                edge = tuple(sorted([u, v]))
                if edge not in seen:
                    edges.append(edge)
                    seen.add(edge)
        return edges
    
    def copy(self) -> 'Graph':
        """Crée une copie du graphe."""
        new_graph = Graph()
        for u in self.adjacency_list:
            for v in self.adjacency_list[u]:
                if not new_graph.has_edge(u, v):
                    new_graph.add_edge(u, v)
        return new_graph
