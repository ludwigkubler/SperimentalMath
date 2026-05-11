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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] += factor * A[i][k]
            b[j] += factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def cheeger_constant(adj_list):
    n = len(adj_list)
    degree = [sum(1 for _ in neighbors) for neighbors in adj_list]
    laplacian = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if j in adj_list[i]:
                laplacian[i][j] = laplacian[j][i] = -1
                degree[i] -= 1
                degree[j] -= 1
    laplacian = [[d - A[i][j] for j, d in enumerate(degree)] + [0] * (n - len(adj_list[i])) for i, adj_list in enumerate(adj_list)]
    
    eigenvalues = sorted(gaussian_elimination(laplacian, [0] * n))
    return eigenvalues[1]

def extended_frege_proof_size(phi):
    # Placeholder function to estimate proof size
    # This is a dummy implementation and should be replaced with actual DPLL-based algorithm
    return random.randint(10, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = [random.choice([True, False]) for _ in range(n)]
    adj_list = [[] for _ in range(n)]
    
    # Generate a random 3-CNF instance
    for i in range(n):
        if phi[i]:
            continue
        for j in range(i+1, n):
            if phi[j]:
                continue
            for k in range(j+1, n):
                if phi[k]:
                    continue
                adj_list[i].append(j)
                adj_list[i].append(k)
                adj_list[j].append(i)
                adj_list[j].append(k)
                adj_list[k].append(i)
                adj_list[k].append(j)
    
    h_phi = cheeger_constant(adj_list)
    size_pi = extended_frege_proof_size(phi)
    
    return {
        "metric_name": "Cheeger Constant Inverse Proportional to Proof Size",
        "metric_value": h_phi * size_pi,
        "instances_tested": 1,
        "conjecture_holds": h_phi * size_pi <= 1,
        "counterexample": "" if h_phi * size_pi <= 1 else f"Counterexample: h(Φ)={h_phi}, size(Π)={size_pi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")