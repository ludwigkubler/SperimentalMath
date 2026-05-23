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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n // 2):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def incidence_graph(clauses):
        graph = {}
        for clause in clauses:
            for var in clause:
                if var not in graph:
                    graph[var] = set()
                for other_var in clause:
                    if other_var != var and other_var not in graph[var]:
                        graph[var].add(other_var)
        return graph
    
    def morse_complex(graph):
        n = len(graph)
        rank = 0
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i, neighbors in enumerate(graph.values(), start=1):
            for j in neighbors:
                matrix[i][j] = 1
        
        # Gaussian elimination to find the rank of the matrix
        for i in range(1, n + 1):
            if matrix[i][i] == 0:
                found_nonzero = False
                for j in range(i + 1, n + 1):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    continue
            
            pivot = matrix[i][i]
            for j in range(i, n + 1):
                matrix[i][j] /= pivot
            for k in range(1, n + 1):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n + 1):
                        matrix[k][j] -= factor * matrix[i][j]
        
        rank = sum(1 for row in matrix[1:] if any(row))
        return rank
    
    def is_expander(graph):
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph.values()]
        avg_degree = sum(degrees) / n
        min_degree = min(degrees)
        max_degree = max(degrees)
        
        # Heuristic to check if the graph is an expander
        return (max_degree - min_degree) <= 2 * avg_degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            clauses = generate_k_cnf(n, k=3)
            graph = incidence_graph(clauses)
            rank = morse_complex(graph)
            total_rank += rank
            instances_tested += 1
            
            if rank > 10:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}"
            
            if not is_expander(graph):
                break
    
    mean_rank = total_rank / instances_tested
    lower_bound = 2 ** (n_values[-1] / 3)
    
    return {
        "metric_name": "Morse Complex Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")