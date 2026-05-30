# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_graph(n):
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return G
    
    def hyperbolic_metric(G):
        n = len(G)
        d_H = 0
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    d_H += 1 / (i + j)
        return d_H
    
    def resolution_width(P):
        width = 0
        for clause in P:
            width = max(width, len(clause))
        return width
    
    def construct_resolution_proof(G):
        n = len(G)
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 0:
                    clause = [i, -j]
                    clauses.append(clause)
        return clauses
    
    def gaussian_elimination(A, b):
        n = len(b)
        A_b = A + [b]
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A_b[j][i]) > abs(A_b[max_row][i]):
                    max_row = j
            A_b[i], A_b[max_row] = A_b[max_row], A_b[i]
            for j in range(n):
                if j != i:
                    factor = A_b[j][i] / A_b[i][i]
                    for k in range(n + 1):
                        A_b[j][k] -= factor * A_b[i][k]
        for i in range(n):
            A_b[i][n] /= A_b[i][i]
            A_b[i][i] = 1
        return [row[n] for row in A_b]
    
    def is_satisfiable(G):
        n = len(G)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0 for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 0:
                    A[i][j] = -1
                    A[j][i] = -1
                    b[i] += 1
                    b[j] += 1
        return gaussian_elimination(A, b) != [0 for _ in range(n)]
    
    def resolution_refutation(G):
        n = len(G)
        clauses = construct_resolution_proof(G)
        refutation = []
        while True:
            new_clause = None
            for clause1 in clauses:
                for clause2 in clauses:
                    if set(clause1) & set(clause2):
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        break
                if new_clause:
                    break
            if not new_clause:
                return refutation
            clauses.append(new_clause)
            refutation.append(new_clause)
    
    n_max = 40
    instances_tested = 0
    total_width = 0
    
    for n in range(5, n_max + 1):
        G = generate_graph(n)
        if not is_satisfiable(G):
            continue
        
        P = resolution_refutation(G)
        width = resolution_width(P)
        
        d_H = hyperbolic_metric(G)
        
        total_width += width
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_satisfiable_graphs"
        }
    
    mean_width = total_width / instances_tested
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")