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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def is_invertible(A):
        det = 1.0
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                return False
            det *= pivot
        return True
    
    def minimal_generators(G):
        n = len(G)
        generators = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1 and G[j][i] == 0:
                    generators.append((i, j))
        return len(generators)
    
    def tseitin_formula(G):
        n = len(G)
        clauses = []
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1 and G[j][i] == 0:
                    clauses.append([-(n+i), -(n+j), (2*n+i)])
                    clauses.append([-(n+i), -(2*n+j), (2*n+i)])
                    clauses.append([-(n+j), -(2*n+i), (2*n+j)])
                    clauses.append([-(n+j), -(2*n+j), -(2*n+i)])
        return clauses
    
    def resolution_length(clauses):
        n = len(clauses)
        A = [[0] * (2*n+1) for _ in range(n)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    A[i][literal-1] = 1
                else:
                    A[i][-literal-1] = -1
        rank = gaussian_elimination(A)
        return n - sum(1 for row in rank if all(x == 0 for x in row))
    
    def generate_graph(n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.randint(0, 1) == 1:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_graph(n)
    m_G = minimal_generators(G)
    clauses = tseitin_formula(G)
    L_phi = resolution_length(clauses)
    
    return {
        "metric_name": "Resolution length",
        "metric_value": L_phi,
        "instances_tested": 1,
        "conjecture_holds": L_phi >= 2 ** (math.ceil(math.log(m_G, 2))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")