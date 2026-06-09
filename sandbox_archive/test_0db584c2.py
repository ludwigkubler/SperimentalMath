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
    
    def generate_frege_proof(depth):
        if depth == 0:
            return []
        else:
            op = random.choice(['+', '*'])
            left = generate_frege_proof(depth - 1)
            right = generate_frege_proof(depth - 1)
            return [op, left, right]
    
    def construct_coxeter_group(proof):
        if not proof:
            return {}
        elif isinstance(proof[0], int):
            return {proof[0]: []}
        else:
            op, left, right = proof
            G_left = construct_coxeter_group(left)
            G_right = construct_coxeter_group(right)
            G = {}
            for x in G_left:
                if x not in G:
                    G[x] = []
                for y in G_left[x]:
                    G[x].append((y, 'L'))
            for x in G_right:
                if x not in G:
                    G[x] = []
                for y in G_right[x]:
                    G[x].append((y, 'R'))
            return G
    
    def rank_coxeter_group(G):
        n = len(G)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for i, neighbors in enumerate(G.values()):
            for neighbor, direction in neighbors:
                if direction == 'L':
                    adjacency_matrix[i][neighbor] = 1
                else:
                    adjacency_matrix[neighbor][i] = 1
        
        def gaussian_elimination(matrix):
            rows, cols = len(matrix), len(matrix[0])
            for i in range(rows):
                # Find pivot row
                max_row = i
                for r in range(i+1, rows):
                    if abs(matrix[r][i]) > abs(matrix[max_row][i]):
                        max_row = r
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                # Eliminate below pivot
                for r in range(i+1, rows):
                    factor = -matrix[r][i] / matrix[i][i]
                    for c in range(cols):
                        if i == c:
                            matrix[r][c] = 0
                        else:
                            matrix[r][c] += factor * matrix[i][c]
        
        gaussian_elimination(adjacency_matrix)
        
        rank = sum(1 for row in adjacency_matrix if any(row))
        return rank
    
    max_depth = 40
    instances_tested = 0
    total_rank = 0
    n_max = 0
    
    for depth in range(5, max_depth + 1):
        proof = generate_frege_proof(depth)
        G = construct_coxeter_group(proof)
        rank = rank_coxeter_group(G)
        
        instances_tested += 1
        total_rank += rank
        n_max = max(n_max, depth)
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = all(rank <= 1.5 * depth ** 1.5 for _, proof in enumerate(proofs) for depth in range(5, max_depth + 1))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")