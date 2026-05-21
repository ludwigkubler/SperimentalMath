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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_random_graph(n: int) -> list:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            G[i][i] = 0
        return G
    
    def is_expander(G: list) -> bool:
        n = len(G)
        degree_sum = sum(sum(row) for row in G)
        avg_degree = degree_sum / n
        if avg_degree < 2 * math.log(n):
            return False
        for i in range(n):
            neighbors = [j for j in range(n) if G[i][j] == 1]
            if len(neighbors) <= 1:
                return False
        return True
    
    def clique_complex(G: list) -> int:
        n = len(G)
        max_length = 0
        for k in range(2, n + 1):
            subsets = itertools.combinations(range(n), k)
            for subset in subsets:
                subgraph = [[G[i][j] for j in subset] for i in subset]
                if all(subgraph[i * (k - 1) + j] == G[subset[i]][subset[j]] for i in range(k - 1) for j in range(i + 1, k)):
                    max_length = max(max_length, k)
        return max_length
    
    def dpll(G: list, assignment: dict, clause_index: int = 0) -> bool:
        if clause_index == len(clauses):
            return True
        literals = clauses[clause_index]
        for literal in literals:
            var = abs(literal) - 1
            if var not in assignment:
                assignment[var] = literal > 0
                if dpll(G, assignment, clause_index + 1):
                    return True
                del assignment[var]
            elif assignment[var] == (literal > 0):
                break
        else:
            for literal in literals:
                var = abs(literal) - 1
                if var not in assignment:
                    assignment[var] = not (literal > 0)
                    if dpll(G, assignment, clause_index + 1):
                        return True
                    del assignment[var]
        return False
    
    def tseitin_formula(G: list) -> str:
        n = len(G)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    clauses.append([-i - 1, -j - 1, i + j + 2])
                    clauses.append([-i - 1, j + 1])
                    clauses.append([i + 1, -j - 1])
        return clauses
    
    def resolution_length(clauses: list) -> int:
        assignment = {}
        timeout = 60
        start_time = time.time()
        if dpll(G, assignment):
            return len(assignment)
        else:
            return float('inf')
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_random_graph(n)
    max_length = clique_complex(G)
    if not is_expander(G):
        max_length = 1
    clauses = tseitin_formula(G)
    length = resolution_length(clauses)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": length >= 2 ** (0.2 * max_length),
        "counterexample": "" if length >= 2 ** (0.2 * max_length) else f"Graph with n={n}, A={G}"
    }

if __name__ == "__main__":
    import sys
    import time
    import itertools
    
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n}, A={G}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")