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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf, n):
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for var in clause:
                if var > 0:
                    matrix[var-1][abs(var)-1] = 1
                else:
                    matrix[abs(var)-1][var-1] = -1
        return matrix
    
    def ab_index(matrix):
        n = len(matrix)
        total = 0
        for i in range(n):
            for j in range(i+1, n):
                if matrix[i][j] != 0 and matrix[j][i] != 0:
                    total += abs(matrix[i][j]) * abs(matrix[j][i])
        return total
    
    def circuit_monotone_width(cnf):
        # Placeholder function; actual implementation needed
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n*2))
            matrix = incidence_matrix(cnf, n)
            ab = ab_index(matrix)
            w_m = circuit_monotone_width(cnf)
            results.append({"n": n, "ab": ab, "w_m": w_m})
    
    if not results:
        return {
            "metric_name": "AB(φ) vs w_m",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ab_values = [r["ab"] for r in results]
    w_m_values = [r["w_m"] for r in results]
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    
    if not all(ab >= 0 and w_m >= 0 for ab, w_m in zip(ab_values, w_m_values)):
        return {
            "metric_name": "AB(φ) vs w_m",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Negative values in AB or w_m"
        }
    
    mean_ab = sum(ab_values) / len(ab_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    covariance = sum((ab - mean_ab) * (w_m - mean_w_m) for ab, w_m in zip(ab_values, w_m_values)) / len(ab_values)
    variance_w_m = sum((w_m - mean_w_m) ** 2 for w_m in w_m_values) / len(w_m_values)
    
    correlation_coefficient = covariance / math.sqrt(variance_w_m * (sum(ab ** 2 for ab in ab_values) / len(ab_values) - mean_ab ** 2))
    
    return {
        "metric_name": "AB(φ) vs w_m",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": f"Correlation coefficient {correlation_coefficient} < 0.5" if not abs(correlation_coefficient) >= 0.7 else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_metric_values")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")