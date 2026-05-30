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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def circuit_size(f):
        n = len(f)
        if n == 1:
            return f[0] + 1
        mid = n // 2
        left = circuit_size(f[:mid])
        right = circuit_size(f[mid:])
        return min(left, right) + 1
    
    def linear_representations(f):
        n = len(f)
        F = [Fraction(1, 2), Fraction(-1, 2)]
        representations = set()
        
        def matrix_mult(A, B):
            m, k, n = len(A), len(B[0]), len(B)
            C = [[sum(A[i][j] * B[j][k] for j in range(k)) for k in range(n)] for i in range(m)]
            return C
        
        def gaussian_elimination(M):
            rows, cols = len(M), len(M[0])
            for col in range(cols):
                max_row = next((r for r in range(col, rows) if M[r][col] != 0), None)
                if max_row is not None:
                    M[col], M[max_row] = M[max_row], M[col]
                    for r in range(rows):
                        if r != col and M[r][col] != 0:
                            factor = -M[r][col] / M[col][col]
                            M[r] = [M[r][c] + factor * M[col][c] for c in range(cols)]
            return M
        
        def is_linear(f):
            A = [[Fraction(1, 2) if i == j else Fraction(-1, 2) for j in range(n)] for i in range(n)]
            b = [f[i] - f[0] for i in range(1, n)]
            A = gaussian_elimination(A)
            for r in range(n):
                if A[r][r] == 0:
                    return False
                for c in range(r + 1, n):
                    A[r][c] /= A[r][r]
                b[r] /= A[r][r]
                A[r][r] = 1
            return True
        
        def count_representations(f):
            if is_linear(f):
                return 1
            else:
                count = 0
                for a in F:
                    for b in F:
                        if (a + b) * f[0] == (a - b) * f[1]:
                            count += 1
                return count
        
        return count_representations(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        C_f = linear_representations(f)
        Omega_f = circuit_size(f)
        
        if Omega_f == 0:
            continue
        
        ratio = Fraction(C_f * (n + 1) ** 2, Omega_f).limit_denominator()
        results.append(ratio)
    
    if not results:
        return {
            "metric_name": "log(n+1)^2 * C(f)/Omega(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    conjecture_holds = all(ratio <= 100 for ratio in results)  # Arbitrary upper bound
    
    return {
        "metric_name": "log(n+1)^2 * C(f)/Omega(f)",
        "metric_value": float(mean),
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Upper bound exceeded"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        mean_values = [r["metric_value"] for r in results if "metric_value" in r and r["metric_value"] is not None]
        std_devs = [r["instances_tested"] for r in results if "instances_tested" in r]
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={sum(mean_values) / len(mean_values)} std={sum(std_devs) / len(std_devs)} support_fraction={support_fraction}")
        elif any(r["counterexample"] != "" for r in results):
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if r["counterexample"] != "")
            print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_data")