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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_matrix_representation(f, n):
    T = [[f[(i >> j) & 1] for j in range(n)] for i in range(2**n)]
    return T

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(rank + 1, m):
            factor = -A[i][j] / A[rank][j]
            for k in range(n):
                A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def compute_communication_complexity_rank(f):
    n = int(math.log2(len(f)))
    T = compute_matrix_representation(f, n)
    comm_rank = gaussian_elimination(T)
    return comm_rank

def alexander_dirac_invariant(A):
    m, n = len(A), len(A[0])
    det = 1
    for i in range(m):
        if A[i][i] == 0:
            continue
        for j in range(i + 1, m):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]
        det *= A[i][i]
    return abs(det)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_comm_rank = 0
    total_alexander_dirac_invariant = 0
    n_max = 0

    for n in n_values:
        f = generate_random_boolean_function(n)
        comm_rank = compute_communication_complexity_rank(f)
        alexander_dirac_inv = alexander_dirac_invariant(compute_matrix_representation(f, n))
        
        instances_tested += 1
        total_comm_rank += comm_rank
        total_alexander_dirac_invariant += alexander_dirac_inv
        n_max = max(n_max, n)

    mean_comm_rank = total_comm_rank / instances_tested
    mean_alexander_dirac_invariant = total_alexander_dirac_invariant / instances_tested

    correlation_coefficient = (instances_tested * sum(c * a for c, a in zip(comm_rank_values, alexander_dirac_inv_values)) -
                               sum(comm_rank_values) * sum(alexander_dirac_inv_values)) / \
                              math.sqrt((instances_tested * sum(c**2 for c in comm_rank_values) - sum(comm_rank_values)**2) *
                                        (instances_tested * sum(a**2 for a in alexander_dirac_inv_values) - sum(alexander_dirac_inv_values)**2))

    conjecture_holds = abs(correlation_coefficient) >= 1.5
    counterexample = "" if conjecture_holds else "correlation_outside_threshold"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_outside_threshold\" first_failing_seed={first_failing_seed}")