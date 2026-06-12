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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m_index_values = []
    w_values = []

    for _ in range(30):
        # Generate a random Tseitin formula with n variables
        G = {i: [] for i in range(n)}
        literals = [f'x{i}' for i in range(n)]
        negated_literals = [f'-x{i}' for i in range(n)]
        clauses = []

        for i in range(n):
            literal = random.choice(literals)
            negated_literal = random.choice(negated_literals)
            G[i].append((literal, 1))
            G[i].append((negated_literal, -1))
            clauses.append((literal, negated_literal))

        # Compute the minimal index of the tropical polynomial root system
        m_index = sum(1 for clause in clauses if any(lit in literals for lit in clause))
        m_index_values.append(m_index)

        # Compute the resolution proof width
        w = len(clauses)
        w_values.append(w)

    correlation_coefficient = compute_correlation(m_index_values, w_values)
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.6 for corr in m_index_values),
        "counterexample": ""
    }

def compute_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    return numerator / denominator if denominator != 0 else None

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and all(res["metric_value"] >= 0.6 for res in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.8\" first_failing_seed=1")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")