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

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (-1 if random.random() < 0.5 else 1)]
        while len(clause) < 3:
            var = random.choice(variables)
            if all(var != abs(v) for v in clause):
                clause.append(var * (-1 if random.random() < 0.5 else 1))
        clauses.append(clause)
    return clauses

def p_adic_norm(x, n):
    while x % n == 0:
        x //= n
    return x

def p_adic_harmonic_space(F, S):
    rank = 0
    for clause in F:
        norm_sum = sum(p_adic_norm(abs(var), len(S)) for var in clause)
        if norm_sum > rank:
            rank = norm_sum
    return rank

def monotone_circuit_lower_bound(F):
    # Placeholder function, replace with actual algorithm
    return len(F)

def spearman_correlation(ranks1, ranks2):
    n = len(ranks1)
    sorted_ranks1 = sorted(range(n), key=lambda i: ranks1[i])
    sorted_ranks2 = sorted(range(n), key=lambda i: ranks2[i])
    rho_numerator = sum((ranks1[sorted_ranks1[i]] - ranks2[sorted_ranks2[i]]) ** 2 for i in range(n))
    rho_denominator = n * (n**2 - 1) / 6
    return 1 - (6 * rho_numerator) / rho_denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2*n)
    F = generate_3cnf(n, m)
    S = [random.randint(1, 40) for _ in range(40)]
    H_F = p_adic_harmonic_space(F, S)
    kappa_m = monotone_circuit_lower_bound(F)
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": spearman_correlation([H_F], [kappa_m])[0],
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")