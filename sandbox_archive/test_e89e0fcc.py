# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique(n, k):
        vertices = list(range(n))
        edges = set()
        for combo in combinations(vertices, 2):
            if len(set(combo)) == 2 and random.random() < (k / n):
                edges.add(tuple(sorted(combo)))
        return vertices, edges
    
    def incidence_matrix(vertices, edges):
        n = len(vertices)
        m = len(edges)
        A = [[0] * m for _ in range(n)]
        edge_dict = {edge: i for i, edge in enumerate(edges)}
        for v in vertices:
            for u in vertices:
                if (v, u) in edges or (u, v) in edges:
                    A[v][edge_dict[(min(v, u), max(v, u))]] = 1
        return A
    
    def submodular_rank(A):
        n = len(A)
        m = len(A[0])
        rank = 0
        for i in range(m):
            max_col = -1
            max_val = -float('inf')
            for j in range(n):
                if A[j][i] > max_val:
                    max_val = A[j][i]
                    max_col = j
            if max_col == -1:
                break
            rank += 1
            for j in range(n):
                if j != max_col:
                    A[j][i] -= A[j][max_col] * A[max_col][i] / A[max_col][max_col]
        return rank
    
    def dpll_solver(A, assignment, clause_count):
        n = len(A)
        m = len(A[0])
        if all(assignment[i] is not None for i in range(n)):
            return True
        var = next(i for i in range(n) if assignment[i] is None)
        for val in [True, False]:
            new_assignment = assignment[:]
            new_assignment[var] = val
            if dpll_solver(A, new_assignment, clause_count):
                return True
        return False
    
    def min_dnf_size(vertices, edges):
        n = len(vertices)
        m = len(edges)
        max_clauses = 2 ** n - 1
        for clause_count in range(1, max_clauses + 1):
            if dpll_solver(incidence_matrix(vertices, edges), [None] * n, clause_count):
                return clause_count
        return float('inf')
    
    def is_monotone_dnf(A):
        n = len(A)
        m = len(A[0])
        for i in range(m):
            max_col = -1
            max_val = -float('inf')
            for j in range(n):
                if A[j][i] > max_val:
                    max_val = A[j][i]
                    max_col = j
            if max_col == -1:
                break
            for j in range(n):
                if j != max_col and A[j][max_col] < A[j][i]:
                    return False
        return True
    
    n = 40
    k = random.randint(2, 5)
    vertices, edges = generate_k_clique(n, k)
    A = incidence_matrix(vertices, edges)
    
    rank = submodular_rank(A)
    dnf_size = min_dnf_size(vertices, edges)
    is_monotone = is_monotone_dnf(A)
    
    return {
        "metric_name": "submodular_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= 0.1 * n and dnf_size <= n**2 and (not is_monotone or dnf_size <= 5 * math.log(n)),
        "counterexample": "" if rank >= 0.1 * n and dnf_size <= n**2 and (not is_monotone or dnf_size <= 5 * math.log(n)) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")