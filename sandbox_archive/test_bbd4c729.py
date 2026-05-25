# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', f'{variables[i]}'])
        return clauses
    
    def configuration_space_metric(clauses):
        points = set()
        distances = {}
        for clause in clauses:
            point = tuple(sorted(clause))
            if point not in points:
                points.add(point)
                for other_point in points:
                    dist = sum(1 for a, b in zip(point, other_point) if a != b)
                    distances[(point, other_point)] = dist
        return points, distances
    
    def min_rank(points, distances):
        n = len(points)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points):
                if (point1, point2) in distances:
                    adjacency_matrix[i][j] = distances[(point1, point2)]
        
        rank = 0
        for i in range(n):
            max_edge = 0
            for j in range(i+1, n):
                if adjacency_matrix[i][j] > max_edge:
                    max_edge = adjacency_matrix[i][j]
            rank += max_edge
        return rank
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            # Find the pivot row
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            # Eliminate below the pivot
            for j in range(i+1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank
    
    def min_rank_gaussian(matrix):
        n = len(matrix)
        augmented_matrix = [row + [1] for row in matrix]
        rank = gaussian_elimination(augmented_matrix)
        return rank
    
    def construct_tseitin_metric(n):
        clauses = tseitin_formula(n)
        points, distances = configuration_space_metric(clauses)
        matrix = [[0] * len(points) for _ in range(len(points))]
        for i, point1 in enumerate(points):
            for j, point2 in enumerate(points):
                if (point1, point2) in distances:
                    matrix[i][j] = distances[(point1, point2)]
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        matrix = construct_tseitin_metric(n)
        rank = min_rank_gaussian(matrix)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank >= n**2 * math.log(n) for rank, n in zip(ranks, n_values))
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={0} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={0} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")