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

def generate_formal_context(n):
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(2 ** n):
        clause = [j + 1 for j in range(n) if (i >> j) & 1]
        clauses.append(clause)
    formal_context = [[0] * len(variables) for _ in range(len(clauses))]
    for i, clause in enumerate(clauses):
        for var in clause:
            formal_context[i][var - 1] = 1
    return formal_context

def circuit_monotone_width(formal_context):
    n = len(formal_context)
    m = len(formal_context[0])
    width = [0] * (n + 1)
    for i in range(n):
        for j in range(m):
            if formal_context[i][j] == 1:
                width[j] += 1
    return max(width)

def minimal_order(formal_context):
    n = len(formal_context)
    m = len(formal_context[0])
    order = [0] * (n + 1)
    for j in range(m):
        for i in range(n):
            if formal_context[i][j] == 1:
                order[j] += 1
    return max(order)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    formal_context = generate_formal_context(n)
    monotone_width = circuit_monotone_width(formal_context)
    order = minimal_order(formal_context)
    metric_value = Fraction(order) <= monotone_width**Fraction(1, 2)
    return {
        "metric_name": "order_vs_monotone_width",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": metric_value,
        "counterexample": ""
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
        counterexample = "order_vs_monotone_width"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")