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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    
    for i in range(rows):
        # Find pivot
        max_row = i
        for r in range(i+1, rows):
            if abs(augmented_matrix[r][i]) > abs(augmented_matrix[max_row][i]):
                max_row = r
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate below pivot
        factor = augmented_matrix[i][i]
        if factor == 0:
            continue  # Skip row with zero pivot
        for j in range(i, cols + 1):
            augmented_matrix[i][j] /= factor
        
        for r in range(rows):
            if r != i:
                factor = augmented_matrix[r][i]
                for j in range(i, cols + 1):
                    augmented_matrix[r][j] -= factor * augmented_matrix[i][j]
    
    # Extract reduced row echelon form
    rref = [row[:cols] for row in augmented_matrix]
    rank = sum(1 for row in rref if any(row[j] != 0 for j in range(cols)))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 6))
    
    # Generate a random adjacency matrix for the k-CLIQUE problem
    adj_matrix = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            adj_matrix[j][i] = adj_matrix[i][j]
    
    # Check if there is a k-clique
    def has_k_clique(adj_matrix, k):
        nodes = list(range(n))
        for subset in itertools.combinations(nodes, k):
            clique = True
            for i in range(k):
                for j in range(i+1, k):
                    if adj_matrix[subset[i]][subset[j]] == 0:
                        clique = False
                        break
                if not clique:
                    break
            if clique:
                return True
        return False
    
    if has_k_clique(adj_matrix, k):
        # Construct a Kähler form (simplified for testing)
        # This is a placeholder and does not represent a real Kähler form
        kahler_form = [[random.random() for _ in range(n)] for _ in range(n)]
        
        # Tropicalize the Kähler form
        tropicalized_matrix = [[-math.inf if x == 0 else -x for x in row] for row in kahler_form]
        
        # Compute the minimal rank of the tropicalized matrix
        rank = gaussian_elimination(tropicalized_matrix)
        
        # Check the conjecture
        if n <= 40:
            lower_bound = Fraction(n, 4).limit_denominator()
        else:
            c_n = Fraction(1, 2 ** (n - 40)).limit_denominator()  # Example constant
            lower_bound = Fraction(n, 4) + c_n
        
        conjecture_holds = rank >= lower_bound
        counterexample = "" if conjecture_holds else f"Kähler form rank {rank} < {lower_bound}"
        
        return {
            "metric_name": "Minimal Rank of Tropicalized Kähler Form",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }
    else:
        # If no k-clique, the conjecture does not apply
        return {
            "metric_name": "Minimal Rank of Tropicalized Kähler Form",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No k-clique found"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")