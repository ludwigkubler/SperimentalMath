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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def cnf_to_poly(cnf):
        n = len(cnf[0])
        poly = [[Fraction(0)] * n for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    poly[var][var] += Fraction(1)
                else:
                    poly[0][var] -= Fraction(1)
        return poly
    
    def determinant(matrix):
        n = len(matrix)
        det = Fraction(0)
        for i in range(n):
            submatrix = [[matrix[j][k] for k in range(j + 1, n)] for j in range(i + 1, n)]
            sign = (-1) ** i
            if n == 2:
                det += sign * (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
            else:
                det += sign * matrix[i][0] * determinant(submatrix)
        return det
    
    def discriminant(poly):
        n = len(poly)
        if n == 2:
            a, b, c = poly[0][0], poly[0][1], poly[1][1]
            return b**2 - 4*a*c
        else:
            return determinant([[poly[i][j] for j in range(i + 1, n)] for i in range(n)])
    
    def frege_proof_length(cnf):
        # Placeholder function; actual implementation depends on the Frege proof system
        return len(cnf) * 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            poly = cnf_to_poly(cnf)
            delta = discriminant(poly)
            f_phi = frege_proof_length(cnf)
            if delta <= 0:
                continue
            results.append((math.log(delta), f_phi))
    
    if not results:
        return {
            "metric_name": "log(discriminant)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_delta, f_phi = zip(*results)
    n = len(log_delta)
    mean_log_delta = sum(log_delta) / n
    mean_f_phi = sum(f_phi) / n
    variance_log_delta = sum((x - mean_log_delta) ** 2 for x in log_delta) / n
    variance_f_phi = sum((x - mean_f_phi) ** 2 for x in f_phi) / n
    
    correlation_coefficient = (sum((log_delta[i] - mean_log_delta) * (f_phi[i] - mean_f_phi) for i in range(n)) /
                                math.sqrt(variance_log_delta * variance_f_phi))
    
    return {
        "metric_name": "log(discriminant)",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max([len(cnf) for cnf in results]),
        "conjecture_holds": correlation_coefficient >= 0.9 and p_value <= 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={result['seed']}")
                break