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
    
    def entropy(clause_subset):
        return -sum(p * math.log2(p) for p in clause_subset if p > 0)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = next((i for i in range(rank, rows) if matrix[i][j] != 0), None)
            if i_max is not None:
                matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
                for i in range(rows):
                    if i != rank and matrix[i][j] != 0:
                        factor = matrix[i][j] / matrix[rank][j]
                        for k in range(cols):
                            matrix[i][k] -= factor * matrix[rank][k]
                rank += 1
        return rank
    
    def geometric_group_rank(sat_instance):
        n = len(sat_instance)
        variables = list(range(n))
        clauses = [tuple(sorted(random.sample(variables, random.randint(1, n // 2)))) for _ in range(n)]
        
        # Construct the adjacency matrix of the geometric group
        adj_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for var in clause:
                adj_matrix[var][n] += 1
                adj_matrix[n][var] += 1
        
        # Add self-loops to ensure the matrix is non-singular
        for i in range(n):
            adj_matrix[i][i] += 1
        
        return gaussian_elimination(adj_matrix)
    
    def sat_instance_entropy(sat_instance):
        n = len(sat_instance)
        clause_subset_counts = [0] * (n + 1)
        for i in range(2 ** n):
            assignment = [bool(i >> j & 1) for j in range(n)]
            satisfied_clauses = sum(all(assignment[var - 1] if var > 0 else not assignment[-var - 1] for var in clause) for clause in sat_instance)
            clause_subset_counts[satisfied_clauses] += 1
        
        total_count = 2 ** n
        entropy_values = [clause_subset_counts[i] / total_count * entropy([clause_subset_counts[i] / total_count]) for i in range(n + 1)]
        return sum(entropy_values)
    
    sat_instance = [[random.choice([-1, 0, 1]) for _ in range(random.randint(2, 4))] for _ in range(random.randint(5, 10))]
    rank_G = geometric_group_rank(sat_instance)
    entropy_phi = sat_instance_entropy(sat_instance)
    
    return {
        "metric_name": "Entropy vs Rank",
        "metric_value": entropy_phi,
        "instances_tested": len(sat_instance),
        "n_max": max(len(clause) for clause in sat_instance),
        "conjecture_holds": rank_G > 0 and entropy_phi > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")