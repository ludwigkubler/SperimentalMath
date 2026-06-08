# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def matrix_representation(f, n):
        M = []
        for x in range(2**n):
            row = []
            for y in range(2**n):
                row.append(int(f[x] == f[y]))
            M.append(row)
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        A = [row[:] for row in M]
        lead = 0
        for r in range(n):
            if lead >= n:
                break
            i = r
            while A[i][lead] == 0:
                i += 1
                if i == n:
                    i = r
                    lead += 1
                    if lead == n:
                        return A, False
            A[r], A[i] = A[i], A[r]
            for i in range(r + 1, n):
                factor = Fraction(A[i][lead], A[r][lead])
                for j in range(lead, n):
                    A[i][j] -= factor * A[r][j]
        return A, True
    
    def rank_variance(M):
        A, success = gaussian_elimination(M)
        if not success:
            return 0
        rank = sum(1 for row in A if any(row))
        return (rank - n) ** 2 / n
    
    def count_automorphic_forms(M):
        n = len(M)
        forms = set()
        for i in range(n):
            for j in range(i + 1, n):
                if all(M[i][k] == M[j][k] for k in range(n)):
                    forms.add(tuple(M[i]))
        return len(forms)
    
    def communication_complexity(f, n):
        M = matrix_representation(f, n)
        return rank_variance(M)
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
        return cov / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        rho_f = communication_complexity(f, n)
        aut_forms = count_automorphic_forms(M)
        results.append((rho_f, aut_forms))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    rho_values, aut_form_counts = zip(*results)
    corr_coeff = correlation_coefficient(rho_values, aut_form_counts)
    support_fraction = sum(1 for cc in corr_coeff if cc >= 0.8) / len(corr_coeff)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
        std_corr_coeff = math.sqrt(sum((result["metric_value"] - mean_corr_coeff) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")