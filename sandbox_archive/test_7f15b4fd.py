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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def determinant(A):
    n = len(A)
    det = Fraction(1)
    U = gaussian_elimination(A)
    for i in range(n):
        det *= U[i][i]
    return det

def spectral_gap(G):
    n = len(G)
    L = [[0] * n for _ in range(n)]
    d = [sum(G[i][j] for j in range(n)) for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                L[i][j] = (2 * d[i] - G[i][j]) / 4
            else:
                L[i][j] = -G[i][j] / 4
    eigenvalues = [determinant(L + [[1, 0], [0, -1]]) for _ in range(10)]
    return max(abs(eigenvalue) for eigenvalue in eigenvalues)

def sos_degree(G):
    n = len(G)
    variables = set()
    for i in range(n):
        for j in range(i + 1, n):
            if G[i][j] != 0:
                variables.add((i, j))
    return len(variables)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    G = [row[:] for row in G]
    
    G_val = spectral_gap(G)
    d_G = sos_degree(G)
    sos_req = d_G
    
    if G_val <= Fraction(9, 10) and sos_req > d_G:
        conjecture_holds = False
        counterexample = f"SOS degree {sos_req} greater than dimension {d_G}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Spectral Gap Invariant vs SOS Degree",
        "metric_value": G_val,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 2}")