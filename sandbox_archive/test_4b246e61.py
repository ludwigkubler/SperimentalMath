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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def seifert_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u][v] = 1
            M[v][u] = 1
        return M
    
    def resolution_proof_length(M):
        m, n = len(M), len(M[0])
        if m != n or any(len(row) != n for row in M):
            raise ValueError("Matrix must be square")
        
        # Gaussian elimination to reduce the matrix
        for i in range(n):
            if M[i][i] == 0:
                return float('inf')  # Singular matrix, no finite resolution proof length
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] -= factor * M[i][k]
        
        # Count the number of non-zero rows
        return sum(1 for row in M if any(row))

    def tseitin_formula(edges, n):
        clauses = []
        for u, v in edges:
            clauses.append([u + 1, -(v + 1)])
            clauses.append([-u - 1, v + 1])
            clauses.append([u + 1, v + 1])
            clauses.append([-u - 1, -(v + 1)])
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        graph_edges = generate_graph(n)
        M = seifert_matrix(graph_edges, n)
        R = resolution_proof_length(M)
        S = len(graph_edges)  # Number of edges as a simple invariant
        
        results.append({
            "n": n,
            "S": S,
            "R": R
        })
    
    total_S = sum(result["S"] for result in results)
    total_R = sum(result["R"] for result in results)
    avg_S = total_S / len(results)
    avg_R = total_R / len(results)
    
    conjecture_holds = all(result["S"] <= 2**n and result["R"] >= n**2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution Proof Length vs Seifert Matrix Size",
        "metric_value": avg_R,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    total_S = sum(result["metric_value"] for result in results)
    total_R = sum(result["instances_tested"] for result in results)
    avg_S = total_S / len(results)
    avg_R = total_R / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_S} std={avg_R} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")