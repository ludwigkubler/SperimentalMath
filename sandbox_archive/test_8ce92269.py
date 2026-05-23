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
    
    def generate_bipartite_graph(n):
        A = [random.randint(0, 1) for _ in range(n)]
        B = [random.randint(0, 1) for _ in range(n)]
        G = [[random.choice([0, 1]) if i != j else 0 for j in range(n)] for i in range(n)]
        return A, B, G
    
    def spectral_gap(G):
        n = len(G)
        L = [[G[i][j] - (A[i] * B[j]) / n for j in range(n)] for i in range(n)]
        eigenvalues = [eigenvalue(L) for _ in range(10)]  # Approximate eigenvalues
        return max(eigenvalues) - min(eigenvalues)
    
    def eigenvalue(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        M = [[M[i][j] - (sum(M[k][j] * M[i][k] for k in range(n)) / n) for j in range(n)] for i in range(n)]
        return max(abs(eigenvalue(M + I)), abs(eigenvalue(M - I)))
    
    def sos_degree(G, ratio):
        n = len(G)
        variables = [f'x{i}' for i in range(n)]
        constraints = []
        objective = 0
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    constraints.append(f'{variables[i]} * {variables[j]} <= {ratio}')
                    objective += variables[i] + variables[j]
        return len(constraints)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A, B, G = generate_bipartite_graph(n)
    G_val = spectral_gap(G)
    
    if G_val <= 0.9:
        sos_d = sos_degree(G, 0.879)
        d_G = sum(abs(A[i] - B[j]) for i in range(n) for j in range(n)) / (n * n)
        conjecture_holds = sos_d <= d_G
    else:
        sos_d = None
        d_G = None
        conjecture_holds = False
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_d if sos_d is not None else 0,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Spectral gap {G_val} > 0.9"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Spectral gap > 0.9' first_failing_seed={first_failing_seed}")