# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for j in range(i+1, n):
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
            for j in range(i+1, n):
                clause = [-literals[i], literals[j]]
                clauses.append(clause)
        return literals, clauses
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            raise ValueError("d must be even for a regular graph")
        G = [[] for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i+1, n):
                if len(G[i]) < d and len(G[j]) < d and (i, j) not in edges:
                    G[i].append(j)
                    G[j].append(i)
                    edges.add((i, j))
        return G
    
    def frege_proof_length(clauses):
        # Simplified estimation of Frege proof length
        return sum(len(clause) for clause in clauses)
    
    def minimal_representation_dimension(G):
        n = len(G)
        if n == 0:
            return 0
        adj_matrix = [[0] * n for _ in range(n)]
        for i, neighbors in enumerate(G):
            for j in neighbors:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1
        
        # Gaussian elimination to find the rank of the adjacency matrix
        rank = 0
        for i in range(n):
            if adj_matrix[i][i] == 0:
                found_nonzero_row = False
                for j in range(i+1, n):
                    if adj_matrix[j][i] != 0:
                        for k in range(n):
                            adj_matrix[i][k], adj_matrix[j][k] = adj_matrix[j][k], adj_matrix[i][k]
                        found_nonzero_row = True
                        break
                if not found_nonzero_row:
                    continue
            
            rank += 1
            denom = adj_matrix[i][i]
            for j in range(n):
                adj_matrix[i][j] /= denom
            
            for j in range(n):
                if i != j:
                    factor = adj_matrix[j][i]
                    for k in range(n):
                        adj_matrix[j][k] -= factor * adj_matrix[i][k]
        
        return rank
    
    n_max = 40
    instances_tested = 30
    total_dim_V = 0
    total_f_phi = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        d = 2 * random.randint(1, n // 2)
        literals, clauses = generate_tseitin_formula(n)
        G = generate_d_regular_graph(n, d)
        
        dim_V = minimal_representation_dimension(G)
        f_phi = frege_proof_length(clauses)
        
        total_dim_V += dim_V
        total_f_phi += f_phi
    
    if instances_tested == 0:
        return {
            "metric_name": "dim(V)/f(φ)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances"
        }
    
    avg_dim_V = total_dim_V / instances_tested
    avg_f_phi = total_f_phi / instances_tested
    
    if abs(avg_dim_V / avg_f_phi - 1) <= Fraction(1, 10):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"dim(V)/f(φ) = {avg_dim_V / avg_f_phi}, expected ≈ 1"
    
    return {
        "metric_name": "dim(V)/f(φ)",
        "metric_value": avg_dim_V / avg_f_phi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")