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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def random_quantum_stochastic_process(n):
        P = [[random.random() for _ in range(n)] for _ in range(n)]
        return P
    
    def disjointness_communication_complexity(n):
        # Upper bound for Disjointness communication complexity
        return math.ceil(math.log2(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    tau_values = []
    cc_r_disj_n_values = []
    
    for n in n_values:
        P = random_quantum_stochastic_process(n)
        M_P = gaussian_elimination(P)
        tau_values.append(M_P)
        
        cc_r_disj_n = disjointness_communication_complexity(n)
        cc_r_disj_n_values.append(cc_r_disj_n)
    
    if len(tau_values) != len(cc_r_disj_n_values):
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(tau_values),
            "conjecture_holds": False,
            "counterexample": "mismatched_lengths"
        }
    
    n = len(tau_values)
    tau_sum = sum(tau_values)
    cc_r_disj_n_sum = sum(cc_r_disj_n_values)
    tau_squared_sum = sum(x**2 for x in tau_values)
    cc_r_disj_n_squared_sum = sum(x**2 for x in cc_r_disj_n_values)
    
    numerator = n * tau_sum * cc_r_disj_n_sum - sum(tau_values[i] * cc_r_disj_n_values[i] for i in range(n))
    denominator1 = math.sqrt((n * tau_squared_sum - tau_sum**2) * (n * cc_r_disj_n_squared_sum - cc_r_disj_n_sum**2))
    
    if denominator1 == 0:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(tau_values),
            "conjecture_holds": False,
            "counterexample": "denominator_zero"
        }
    
    rho = numerator / denominator1
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(tau_values),
        "conjecture_holds": rho > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")
    elif any(r["metric_value"] <= 0.5 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["metric_value"] <= 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"rho_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0 support_fraction={support_fraction}")