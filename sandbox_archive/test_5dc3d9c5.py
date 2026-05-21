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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = 1 / A[i][i]
            for j in range(n):
                A[i][j] *= factor
            b[i] *= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return [b[i] / A[i][i] for i in range(n)]

    def hypergeometric_moment(p, k):
        if p <= 0 or k < 0:
            return 0
        return math.comb(k + p - 1, k) / math.comb(p, k)

    n = random.randint(5, 40)
    F = complex

    # Generate a random ACC circuit with n variables
    # This is a placeholder function; actual implementation depends on the conjecture's specifics
    def generate_ACC_circuit(n):
        return [random.choice([1, -1]) for _ in range(n)]

    acc_circuit = generate_ACC_circuit(n)
    characteristic_poly = sum(a * (x ** i) for i, a in enumerate(acc_circuit))
    
    # Calculate the sum of moments of the characteristic polynomial
    moments_sum = sum(hypergeometric_moment(abs(coeff), n) for coeff in [characteristic_poly.real, characteristic_poly.imag])
    
    # For CNF formulas, generate a random CNF formula with n variables
    def generate_CNF_formula(n):
        return [[random.choice([1, -1]) * i for i in range(1, n + 1)] for _ in range(random.randint(5, 10))]

    cnf_formula = generate_CNF_formula(n)
    
    # Calculate the hypergeometric function moments of the defining polynomials
    cnf_moments_sum = sum(hypergeometric_moment(len(clause), n) for clause in cnf_formula)
    
    metric_value_acc = moments_sum / (n * math.log(n))
    metric_value_cnf = cnf_moments_sum / math.log(n)
    
    return {
        "metric_name": "moments_bound",
        "metric_value_acc": metric_value_acc,
        "metric_value_cnf": metric_value_cnf,
        "instances_tested": 1,
        "conjecture_holds_acc": metric_value_acc <= 0.01 * n * math.log(n),
        "counterexample_acc": "" if metric_value_acc <= 0.01 * n * math.log(n) else f"ACC circuit with n={n} violated the bound",
        "conjecture_holds_cnf": metric_value_cnf <= 0.01 * math.log(n),
        "counterexample_cnf": "" if metric_value_cnf <= 0.01 * math.log(n) else f"CNF formula with n={n} violated the bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results_acc = []
    results_cnf = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "metric_value_acc" in result:
            results_acc.append(result["metric_value_acc"])
        if "metric_value_cnf" in result:
            results_cnf.append(result["metric_value_cnf"])
    
    mean_acc = sum(results_acc) / len(results_acc)
    std_acc = math.sqrt(sum((x - mean_acc) ** 2 for x in results_acc) / len(results_acc))
    support_fraction_acc = sum(1 for x in results_acc if x <= 0.01 * n * math.log(n)) / len(results_acc)
    
    mean_cnf = sum(results_cnf) / len(results_cnf)
    std_cnf = math.sqrt(sum((x - mean_cnf) ** 2 for x in results_cnf) / len(results_cnf))
    support_fraction_cnf = sum(1 for x in results_cnf if x <= 0.01 * math.log(n)) / len(results_cnf)
    
    if all(result["conjecture_holds_acc"] for result in results_acc):
        print(f"RESULT: SUPPORTED mean={mean_acc} std={std_acc} support_fraction={support_fraction_acc}")
    elif any(not result["conjecture_holds_acc"] for result in results_acc):
        first_failing_seed = next(seed for seed, result in enumerate(results_acc) if not result["conjecture_holds_acc"])
        print(f"RESULT: FALSIFIED counterexample=\"ACC circuit\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")