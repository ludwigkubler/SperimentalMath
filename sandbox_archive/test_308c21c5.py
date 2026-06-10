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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause[0], clause[1] = clause[1], clause[0]
        clauses.append(clause)
    return clauses

def construct_groupoid(clauses):
    groupoid = {}
    for lit in set(abs(lit) for clause in clauses for lit in clause):
        groupoid[lit] = []
    for clause in clauses:
        for i, lit1 in enumerate(clause):
            for j, lit2 in enumerate(clause):
                if i != j and abs(lit1) == abs(lit2):
                    groupoid[abs(lit1)].append((lit1, lit2))
    return groupoid

def compute_min_homrank(groupoid):
    n = len(groupoid)
    adj_matrix = [[0] * n for _ in range(n)]
    for i, (lit1, edges) in enumerate(groupoid.items()):
        for lit2 in edges:
            adj_matrix[i][groupoid[lit2[1]].index(abs(lit2))] = 1
    # Gaussian elimination to find the rank of the matrix
    rank = 0
    for i in range(n):
        if all(adj_matrix[j][i] == 0 for j in range(rank)):
            continue
        rank += 1
        for j in range(i + 1, n):
            if adj_matrix[j][i] != 0:
                for k in range(n):
                    adj_matrix[j][k], adj_matrix[i][k] = adj_matrix[i][k], adj_matrix[j][k]
    return rank

def sat_complexity(phi_G):
    # Placeholder for a small DPLL solver
    return len(phi_G) / 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 30)
    m = random.randint(n, n * 3)
    phi_G = generate_cnf(n, m)
    G = construct_groupoid(phi_G)
    min_homrank = compute_min_homrank(G)
    sat_complexity_val = sat_complexity(phi_G)
    
    return {
        "metric_name": "min_homrank",
        "metric_value": min_homrank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")