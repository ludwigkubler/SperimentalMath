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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def compute_quasi_quadratic_form(f):
    n = int(math.log2(len(f)))
    Q_f = [[0] * (2*n) for _ in range(2*n)]
    for i in range(2*n):
        for j in range(2*n):
            if 0 <= i + j - n < 2**n:
                Q_f[i][j] = sum(f[k] * f[(k + j - i) % (2**n)] for k in range(2**n))
    return Q_f

def compute_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    for col in range(n):
        if any(matrix[row][col] != 0 for row in range(m)):
            rank += 1
            for row in range(m):
                if matrix[row][col] != 0:
                    factor = Fraction(matrix[row][col], matrix[rank-1][col])
                    for j in range(n):
                        matrix[row][j] -= factor * matrix[rank-1][j]
    return rank

def compute_ac0_circuit_size(f):
    n = int(math.log2(len(f)))
    # Simplified AC0 circuit size estimation
    return 2**n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_size = 0
    count_supporting = 0
    counterexample = ""

    for n in n_values:
        f = generate_boolean_function(n)
        Q_f = compute_quasi_quadratic_form(f)
        R_Q_f = compute_rank(Q_f)
        ac0_circuit_size = compute_ac0_circuit_size(f)

        if R_Q_f == 0 or ac0_circuit_size <= 0:
            continue

        lower_bound = Fraction(2**(R_Q_f), 2**(0.75 * n))
        if ac0_circuit_size < lower_bound:
            counterexample = f"n={n}, R(Q_f)={R_Q_f}, AC0 size={ac0_circuit_size}"
            break
        else:
            total_size += ac0_circuit_size
            count_supporting += 1

    metric_value = total_size / len(n_values)
    conjecture_holds = count_supporting >= 4 and metric_value <= 1.5 * lower_bound

    return {
        "metric_name": "AC0 circuit size",
        "metric_value": float(metric_value),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")

    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")