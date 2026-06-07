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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return A
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            if det == 0:
                return 0
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
        return det
    
    def grothendieck_witt_class_mod_2(matrix):
        det = determinant(matrix)
        if det == 0:
            return 0
        elif det > 0:
            return 1
        else:
            return -1
    
    def dpll_proof_path_length(cnf):
        stack = []
        for clause in cnf:
            if not any(var in stack or -var in stack for var in clause):
                stack.append(random.choice(clause))
        return len(stack)
    
    def hodge_index(n):
        # Simplified Hodge index calculation based on n
        return n
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            hodge = grothendieck_witt_class_mod_2([[var % 2 for var in clause] for clause in cnf])
            dpll_path_length = dpll_proof_path_length(cnf)
            results.append((hodge, dpll_path_length))
    
    if not results:
        return {
            "metric_name": "Hodge Index vs DPLL Path Length",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    hodge_values = [h for h, _ in results]
    dpll_path_lengths = [d for _, d in results]
    
    def rank(x):
        return sorted(x).index(x)
    
    hodge_ranks = [rank(h) for h in hodge_values]
    dpll_ranks = [rank(d) for d in dpll_path_lengths]
    
    correlation_coefficient = sum((h - mean_hodge) * (d - mean_dpll) for h, d in zip(hodge_values, dpll_path_lengths)) / len(results)
    mean_absolute_difference = sum(abs(hr - dr) for hr, dr in zip(hodge_ranks, dpll_ranks)) / len(results)
    
    return {
        "metric_name": "Hodge Index vs DPLL Path Length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and mean_absolute_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE <reason>")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")