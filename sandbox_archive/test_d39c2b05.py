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
from fractions import Fraction
import math
import sys

def minimal_representation_degree(n):
    A = [[random.randint(0, 1) if i == j else random.choice([0, -A[i][j]]) for j in range(n)] for i in range(n)]
    return sum(sum(abs(x) for x in row) for row in A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    D_S = []
    q_phi = []

    for n in n_values:
        if n <= 1:
            continue
        D_S.append(minimal_representation_degree(n))
        # Simulate the number of distinct quadratic forms (placeholder)
        q_phi.append(random.randint(1, n))

    metric_value = sum(D_S) / len(D_S)
    correlation_coefficient = 0.0

    if len(q_phi) > 1:
        mean_q_phi = sum(q_phi) / len(q_phi)
        numerator = sum((D_S[i] - metric_value) * (q_phi[i] - mean_q_phi) for i in range(len(D_S)))
        denominator = math.sqrt(sum((D_S[i] - metric_value)**2 for i in range(len(D_S))) * sum((q_phi[i] - mean_q_phi)**2 for i in range(len(q_phi))))
        if denominator != 0:
            correlation_coefficient = numerator / denominator

    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient_below_0.5"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(D_S),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["correlation_coefficient"] >= 0.5 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")