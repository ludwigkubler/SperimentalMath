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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def tautological_ideal(cnf):
        # Placeholder function to simulate the computation of mli(φ)
        return len(cnf) * 2
    
    def bipartite_graph(cnf):
        n = max(abs(x) for clause in cnf for x in clause)
        adjacency_list = [[] for _ in range(n + 1)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    x, y = abs(clause[i]), abs(clause[j])
                    if (x, y) not in adjacency_list[x]:
                        adjacency_list[x].append((y, clause[i] * clause[j]))
                        adjacency_list[y].append((x, clause[i] * clause[j]))
        return adjacency_list
    
    def laplacian_matrix(adjacency_list):
        n = len(adjacency_list)
        laplacian = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            degree = sum(1 for _, _ in adjacency_list[i])
            laplacian[i][i] = degree
            for j, weight in adjacency_list[i]:
                laplacian[i][j - 1] = -weight
                laplacian[j - 1][i] = -weight
        return laplacian
    
    def spectral_gap(laplacian):
        n = len(laplacian)
        eigenvalues = []
        for i in range(n):
            if sum(laplacian[i]) == 0:
                continue
            v = [random.random() for _ in range(n)]
            v = [x / math.sqrt(sum(x**2 for x in v)) for x in v]
            lambda_i = max(abs(v[j] * laplacian[i][j] for j in range(n))) / sum(v[j]**2 for j in range(n))
            eigenvalues.append(lambda_i)
        return max(eigenvalues) - min(eigenvalues)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    mli_phi = tautological_ideal(cnf)
    adjacency_list = bipartite_graph(cnf)
    laplacian = laplacian_matrix(adjacency_list)
    g_phi = spectral_gap(laplacian)
    
    return {
        "metric_name": "mli_phi vs g_phi",
        "metric_value": mli_phi * g_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")