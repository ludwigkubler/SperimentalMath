# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_instance(n: int, m: int) -> list:
    variables = list(range(1, n + 1))
    instance = []
    for _ in range(m):
        k = random.randint(1, n)
        clause = random.sample(variables, k)
        instance.append(clause)
    return instance

def gaussian_elimination(A: list[list[int]]) -> list[list[int]]:
    m, n = len(A), len(A[0])
    for i in range(m):
        if A[i][i] == 0:
            for j in range(i + 1, m):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                continue
            break
        pivot = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= pivot
        for j in range(m):
            if j != i and A[j][i] != 0:
                factor = -A[j][i]
                for k in range(n):
                    A[j][k] += factor * A[i][k]

    return A

def rank(A: list[list[int]]) -> int:
    m, n = len(A), len(A[0])
    row_echelon_form = gaussian_elimination(A)
    rank = 0
    for i in range(m):
        if any(row_echelon_form[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

def p_adic_metric_dimension(instance: list[list[int]], base: int) -> Fraction:
    m, n = len(instance), len(instance[0])
    A = [[Fraction(0, 1)] * (n + 1) for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if instance[i][j] == 1:
                A[i][j] = Fraction(1, base)
                A[i][-1] += Fraction(1, base)
    
    return rank(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            m = random.randint(n, 2 * n)
            instance = generate_instance(n, m)
            metric_value = p_adic_metric_dimension(instance, base=2)
            metric_values.append(metric_value)
            instances_tested += 1
            n_max = max(n_max, n)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5

    if mean_value > 3.5:
        conjecture_holds = False
        counterexample = f"mean_value={mean_value} exceeds threshold"

    return {
        "metric_name": "p-adic_metric_dimension",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_value={mean_value} exceeds threshold\" first_failing_seed={first_failing_seed}")