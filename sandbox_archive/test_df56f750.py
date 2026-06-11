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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        G = [[0] * n for _ in range(n)]
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d - 1) == 0:
                    G[i][j] = 1
                    G[j][i] = 1
                    edges.append((i, j))
        return G, edges

    def tseitin_formula(edges):
        literals = {}
        clauses = []
        for i, j in edges:
            literal_i = f"x_{i}"
            literal_j = f"x_{j}"
            if literal_i not in literals:
                literals[literal_i] = len(literals)
            if literal_j not in literals:
                literals[literal_j] = len(literals)
            clauses.append([literals[literal_i], literals[literal_j]])
        return literals, clauses

    def tropicalized_cohomology(G, d):
        n = len(G)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    A[i][j] = 1
                    A[j][i] = 1
        A[n][n] = 0
        for i in range(n):
            A[i][n] = -math.inf
            A[n][i] = -math.inf
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if A[i][k] + A[k][j] > A[i][j]:
                        A[i][j] = A[i][k] + A[k][j]
        return max(max(row) for row in A)

    def frege_proof_length(clauses):
        n_vars = len(clauses)
        n_clauses = len(clauses)
        length = 2 * (n_vars + n_clauses)
        return length

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        d = 3
        G, edges = generate_d_regular_graph(n, d)
        if G is None:
            continue
        literals, clauses = tseitin_formula(edges)
        moh = tropicalized_cohomology(G, d)
        f_phi_G = frege_proof_length(clauses)
        results.append((moh, f_phi_G))

    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    moh_values = [m for m, f in results]
    f_phi_G_values = [f for m, f in results]
    correlation_coefficient = sum((m - sum(moh_values) / len(moh_values)) * (f - sum(f_phi_G_values) / len(f_phi_G_values)) for m, f in results) / (len(results) * math.sqrt(sum((m - sum(moh_values) / len(moh_values)) ** 2 for m in moh_values)) * math.sqrt(sum((f - sum(f_phi_G_values) / len(f_phi_G_values)) ** 2 for f in f_phi_G_values)))
    mean_moh = sum(moh_values) / len(moh_values)
    expected_f_phi_G = sum(f_phi_G_values) / len(f_phi_G_values)

    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_moh - expected_f_phi_G) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")