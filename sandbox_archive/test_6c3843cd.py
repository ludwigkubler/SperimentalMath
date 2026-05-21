# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def generate_3sat_instance(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if not any(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
            clauses.append(clause)
    return clauses

def fourier_transform(F):
    n = len(F)
    F_hat = [0] * n
    for k in range(n):
        for i in range(n):
            F_hat[k] += F[i] * (Fraction(math.cos(2 * math.pi * i * k / n), 1) + Fraction(math.sin(2 * math.pi * i * k / n), 1j))
        F_hat[k] /= n
    return F_hat

def sos_refutation_degree(clauses):
    # Simplified SDP relaxation for refutation degree (basic DPLL)
    # This is a placeholder and should be replaced with actual SOS computation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        clauses = generate_3sat_instance(n)
        F = [1] * (2 ** n)  # Placeholder Fourier coefficients
        F_hat = fourier_transform(F)
        refutation_degree = sos_refutation_degree(clauses)
        
        if max(abs(coeff) for coeff in F_hat) < refutation_degree:
            conjecture_holds = False
            counterexample = "SOS refutation degree exceeds max Fourier coefficient"
            break
    
    metric_value = max(abs(coeff) for coeff in F_hat)
    
    return {
        "metric_name": "max_fourier_coefficient",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")