"""
Module: visualization.py
Description: Visualisation des labyrinthes en ASCII et avec Tkinter
"""

from typing import Optional
from .labyrinth import Labyrinth


class LabyrinthVisualizer:
    """Visualisation en ASCII."""
    
    @staticmethod
    def draw_ascii(labyrinth: Labyrinth, show_solution: bool = False) -> str:
        """
        Dessine le labyrinthe en ASCII art.
        
        Format:
          '#' = mur
          'S' = départ
          'E' = sortie
          '*' = chemin solution (si show_solution=True)
          ' ' = passage
        
        Args:
            labyrinth: Labyrinthe à dessiner
            show_solution: Afficher le chemin solution
        
        Returns:
            str: Représentation ASCII
        """
        width = labyrinth.width
        height = labyrinth.height
        graph = labyrinth.graph
        solution_set = set(labyrinth.get_solution() or [])
        
        # Créer la grille
        grid = []
        for y in range(height * 2 + 1):
            row = []
            for x in range(width * 2 + 1):
                row.append('#')
            grid.append(row)
        
        # Remplir les cellules
        for y in range(height):
            for x in range(width):
                cell = y * width + x
                gx, gy = x * 2 + 1, y * 2 + 1
                
                if cell == labyrinth.start:
                    grid[gy][gx] = 'S'
                elif cell == labyrinth.end:
                    grid[gy][gx] = 'E'
                elif show_solution and cell in solution_set:
                    grid[gy][gx] = '*'
                else:
                    grid[gy][gx] = ' '
        
        # Remplir les passages entre cellules
        for y in range(height):
            for x in range(width):
                cell = y * width + x
                
                # Droite
                if x < width - 1 and graph.has_edge(cell, cell + 1):
                    grid[y * 2 + 1][x * 2 + 2] = ' '
                
                # Bas
                if y < height - 1 and graph.has_edge(cell, cell + width):
                    grid[y * 2 + 2][x * 2 + 1] = ' '
        
        return '\n'.join(''.join(row) for row in grid)
    
    @staticmethod
    def print_info(labyrinth: Labyrinth) -> None:
        """Affiche les informations du labyrinthe."""
        info = labyrinth.get_info()
        print("\n" + "=" * 50)
        print("INFORMATIONS DU LABYRINTHE")
        print("=" * 50)
        print(f"Dimensions: {info['width']}x{info['height']}")
        print(f"Nombre total de cases: {info['total_cells']}")
        print(f"Nombre de sommets: {info['num_vertices']}")
        print(f"Nombre d'arêtes (connexions): {info['num_edges']}")
        print(f"Connexité: {'Oui' if info['is_connected'] else 'Non'}")
        print(f"Algorithme de génération: {info['generation_algorithm']}")
        print("=" * 50)
    
    @staticmethod
    def print_solution(labyrinth: Labyrinth) -> None:
        """Affiche les infos de la solution."""
        info = labyrinth.get_info()
        if info['solution_length'] is None:
            print("❌ Aucune solution trouvée!")
        else:
            print("\n" + "=" * 50)
            print("SOLUTION DU LABYRINTHE")
            print("=" * 50)
            print(f"Chemin trouvé: {labyrinth.get_solution()}")
            print(f"Longueur du chemin: {info['solution_length']} cases")
            print(f"Algorithme utilisé: {info['solution_algorithm']}")
            print("=" * 50)
    
    @staticmethod
    def export_to_file(labyrinth: Labyrinth, filename: str, show_solution: bool = False) -> None:
        """Exporte le labyrinthe dans un fichier."""
        with open(filename, 'w') as f:
            f.write(LabyrinthVisualizer.draw_ascii(labyrinth, show_solution))
