#!/usr/bin/env python3
"""
main.py : Point d'entrée principal du projet de labyrinthes

Université de Rouen - L3 Informatique
Module : Application informatique
Méthodes issues de la théorie des graphes pour décrire, générer ou résoudre un labyrinthe

Usage:
    python3 main.py                          # Lancer la GUI
    python3 main.py --cli                    # Mode ligne de commande
    python3 main.py --width 10 --height 10 --algo dfs --solve bfs
    python3 main.py --help                   # Aide
"""

import sys
import argparse
from src.labyrinth import Labyrinth
from src.visualization import LabyrinthVisualizer


def main_cli(args):
    """Mode ligne de commande."""
    print("\n" + "=" * 70)
    print("GÉNÉRATEUR ET RÉSOLVEUR DE LABYRINTHES")
    print("Méthodes issues de la théorie des graphes")
    print("Université de Rouen - L3 Informatique")
    print("=" * 70)
    
    # Créer le labyrinthe
    print(f"\n[1] Création du labyrinthe {args.width}×{args.height}...")
    labyrinth = Labyrinth(args.width, args.height)
    
    # Générer
    print(f"[2] Génération avec {args.algo.upper()}...")
    if args.algo == 'dfs':
        labyrinth.generate_dfs()
    elif args.algo == 'kruskal':
        labyrinth.generate_kruskal()
    else:  # prim
        labyrinth.generate_prim()
    
    # Afficher infos
    LabyrinthVisualizer.print_info(labyrinth)
    
    # Afficher labyrinthe
    print("\n[3] Visualisation du labyrinthe:")
    print(LabyrinthVisualizer.draw_ascii(labyrinth))
    
    # Résoudre
    print(f"\n[4] Résolution avec {args.solve.upper()}...")
    if args.solve == 'bfs':
        labyrinth.solve_bfs()
    elif args.solve == 'dijkstra':
        labyrinth.solve_dijkstra()
    else:  # dfs
        labyrinth.solve_dfs()
    
    # Afficher solution
    LabyrinthVisualizer.print_solution(labyrinth)
    
    # Afficher avec solution
    print("\n[5] Labyrinthe avec solution (* = chemin):")
    print(LabyrinthVisualizer.draw_ascii(labyrinth, show_solution=True))
    
    # Exporter si demandé
    if args.export:
        print(f"\n[6] Exportation vers {args.export}...")
        LabyrinthVisualizer.export_to_file(labyrinth, args.export, show_solution=True)
        print("✓ Exporté!")
    
    print("\n" + "=" * 70)
    print("Fin du programme")
    print("=" * 70 + "\n")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(
        description='Générateur et résolveur de labyrinthes via théorie des graphes',
        epilog='Exemples:\n'
               '  python3 main.py\n'
               '  python3 main.py --cli --width 15 --height 15 --algo kruskal --solve bfs\n'
               '  python3 main.py --cli --export output.txt',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--cli', action='store_true', help='Mode ligne de commande')
    parser.add_argument('--width', type=int, default=12, help='Largeur (défaut: 12)')
    parser.add_argument('--height', type=int, default=12, help='Hauteur (défaut: 12)')
    parser.add_argument('--algo', type=str, default='dfs', 
                       choices=['dfs', 'kruskal', 'prim'],
                       help='Algorithme de génération (défaut: dfs)')
    parser.add_argument('--solve', type=str, default='bfs',
                       choices=['bfs', 'dijkstra', 'dfs'],
                       help='Algorithme de résolution (défaut: bfs)')
    parser.add_argument('--export', type=str, default=None,
                       help='Exporter dans un fichier')
    
    args = parser.parse_args()
    
    # Mode CLI demandé
    if args.cli:
        main_cli(args)
        return
    
    # Sinon: lancer la GUI
    try:
        from src.gui import run_gui
        print("Lancement de l'interface graphique...")
        run_gui()
    except Exception as e:
        print(f"Erreur lors du lancement de la GUI: {e}")
        print("Basculement en mode CLI...")
        main_cli(args)


if __name__ == '__main__':
    main()
