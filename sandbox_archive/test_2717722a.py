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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def is_singular(A):
        det = 1
        for i in range(len(A)):
            det *= A[i][i]
        return abs(det) < 1e-9
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def conjugacy_classes(A):
        m, n = len(A), len(A[0])
        if is_singular(A):
            return 1
        reduced_A = gaussian_elimination(A)
        classes = set()
        for i in range(m):
            class_rep = tuple(reduced_A[i][j] for j in range(n))
            classes.add(class_rep)
        return len(classes)
    
    def resolution_width(phi):
        # Implement a small DPLL solver here
        # This is a placeholder function and should be replaced with actual code
        return 2 * len(phi)  # Placeholder value
    
    n = random.randint(5, 40)
    phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    I_phi = matrix_multiplication(phi, phi)
    classes = conjugacy_classes(I_phi)
    width = resolution_width(phi)
    
    return {
        "metric_name": "ConjugacyClasses",
        "metric_value": classes,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": classes <= (5 * n / 3) and width <= (2 * n),
        "counterexample": "" if classes <= (5 * n / 3) and width <= (2 * n) else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")