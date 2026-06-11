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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    fsi_values = []
    ec_values = []

    while len(fsi_values) < 30:
        phi = generate_random_cnf(n)
        permutation_representation = get_permutation_representation(phi)
        fsi_value = calculate_frobenius_schur_indicator(permutation_representation)
        ec_value = simulate_boolean_circuit_entanglement_complexity(phi)

        if fsi_value is not None and ec_value is not None:
            fsi_values.append(fsi_value)
            ec_values.append(ec_value)
            instances_tested += 1

        n += 5  # Increase the size for the next trial

    correlation_coefficient = calculate_correlation(fsi_values, ec_values)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n - 5,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

def generate_random_cnf(n):
    num_clauses = random.randint(1, n)
    phi = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        phi.append(clause)
    return phi

def get_permutation_representation(phi):
    # Placeholder for actual permutation representation calculation
    return None

def calculate_frobenius_schur_indicator(permutation_representation):
    # Placeholder for actual FSI calculation
    return None

def simulate_boolean_circuit_entanglement_complexity(phi):
    # Placeholder for actual EC simulation
    return None

def calculate_correlation(fsi_values, ec_values):
    n = len(fsi_values)
    if n < 2:
        return None

    mean_fsi = sum(fsi_values) / n
    mean_ec = sum(ec_values) / n
    variance_fsi = sum((x - mean_fsi) ** 2 for x in fsi_values) / (n - 1)
    variance_ec = sum((y - mean_ec) ** 2 for y in ec_values) / (n - 1)

    if variance_fsi == 0 or variance_ec == 0:
        return None

    covariance = sum((fsi_values[i] - mean_fsi) * (ec_values[i] - mean_ec) for i in range(n)) / (n - 1)
    correlation_coefficient = covariance / math.sqrt(variance_fsi * variance_ec)

    return correlation_coefficient

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={sum((r['metric_value'] - mean_d) ** 2 for r in results) / len(results)} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed + 1}")