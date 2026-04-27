# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def generate_unsat_cnf(n, m):
    while True:
        clauses = set()
        for _ in range(m):
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(l in clause for clause in clauses):
                continue
            clauses.add(tuple(sorted(literals)))
        if len(clauses) == m:
            return clauses

def walsh_hadamard_transform(k_F):
    n = len(k_F)
    k_F_hat = [0] * n
    for i in range(n):
        for j in range(n):
            k_F_hat[i] += k_F[j] * math.cos(math.pi * (i & j) / n)
    return k_F_hat

def compute_fourier_variance_ratio(k_F_hat):
    k_F_hat_0 = k_F_hat[0]
    sum_k_F_hat_squared = sum(k_F_hat[i]**2 for i in range(1, len(k_F_hat)))
    return sum_k_F_hat_squared / k_F_hat_0**2

def d_T(F, partial_assignment):
    if not F:
        return 0
    min_depth = float('inf')
    for clause in F:
        covered = True
        for literal in clause:
            var = abs(literal)
            if var not in partial_assignment or partial_assignment[var] != (literal > 0):
                covered = False
                break
        if covered:
            continue
        min_depth = min(min_depth, 1 + d_T(F - {clause}, partial_assignment))
    return min_depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    m_over_n = 4.26
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = int(n * m_over_n)
        F = generate_unsat_cnf(n, m)
        k_F = [0] * (1 << n)
        for clause in F:
            for assignment in range(1 << n):
                if all(lit == 2 or lit == -2 or ((lit > 0) == (assignment & (1 << abs(lit) - 1))) for lit in clause):
                    k_F[assignment] += 1
        k_F_hat = walsh_hadamard_transform(k_F)
        R_F = compute_fourier_variance_ratio(k_F_hat)
        d_T_value = d_T(F, {})
        expected_depth = math.ceil(math.log2(1 / R_F)) + 1

        instances_tested += 1
        if d_T_value < expected_depth:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, d_T={d_T_value}, expected_depth={expected_depth}"

    return {
        "metric_name": "d_T vs R(F)",
        "metric_value": -math.log2(R_F),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE insufficient data")