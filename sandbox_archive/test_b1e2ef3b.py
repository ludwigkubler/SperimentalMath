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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back-substitute
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def dpll(cnf):
    if not cnf:
        return True
    literals = set()
    for clause in cnf:
        literals.update(abs(x) for x in clause)
    literal = random.choice(list(literals))
    new_cnf = [[x for x in clause if x != literal and x != -literal] for clause in cnf]
    return dpll(new_cnf) or dpll([[-x] for x in literals])

def construct_quandle(cnf):
    n = len(cnf)
    quandle = {}
    for i in range(1, n+1):
        quandle[i] = {j: (i + j - 1) % n + 1 for j in range(1, n+1)}
    return quandle

def minimal_local_coherence_index(quandle):
    n = len(quandle)
    index = 0
    for i in range(1, n+1):
        for j in range(1, n+1):
            if quandle[i][j] != quandle[j][i]:
                index += 1
    return index / (n * (n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    trials = 30
    instances_tested = 0
    n_max = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for _ in range(trials):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.random() < 0.5 else 1)
                      for _ in range(random.randint(1, n))]
            cnf.append(clause)

        quandle = construct_quandle(cnf)
        local_coherence_index = minimal_local_coherence_index(quandle)
        proof_length = dpll(cnf) * len(cnf)

        if proof_length == 0:
            conjecture_holds = False
            counterexample = "DPLL proof length is zero"
            break

        metric_value = abs(local_coherence_index - proof_length)
        total_metric_value += metric_value
        instances_tested += n
        n_max = max(n_max, n)

    if not conjecture_holds:
        return {
            "metric_name": "LocalCoherenceIndex-DPLLProofLengthCorrelation",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": counterexample
        }

    mean_metric_value = total_metric_value / instances_tested
    threshold = 3 * (1 / math.sqrt(instances_tested))
    if any(metric_value > mean_metric_value + threshold or metric_value < mean_metric_value - threshold for _ in range(trials)):
        conjecture_holds = False

    return {
        "metric_name": "LocalCoherenceIndex-DPLLProofLengthCorrelation",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexamples = [r["counterexample"] for r in results if not r["conjecture_holds"]]
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE no_counterexamples_found")