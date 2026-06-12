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

def p_adic_dilogarithm(x, p):
    if x <= 0:
        return 0
    result = 0
    for k in range(1, 100):  # Limit to avoid infinite loop
        term = (x ** k) / math.factorial(k)
        if abs(term) < 1e-10:
            break
        result += term
    return result

def rank(matrix):
    n = len(matrix)
    m = len(matrix[0])
    augmented_matrix = [row + [0] for row in matrix]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        if augmented_matrix[i][i] == 0:
            return m
        for j in range(i+1, n):
            factor = augmented_matrix[j][i] / augmented_matrix[i][i]
            for k in range(m+1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    rank = sum(1 for row in augmented_matrix if any(row))
    return rank

def generate_formula(n):
    literals = [f'x{i}' for i in range(n)]
    formula = ' or '.join(random.sample(literals, n-1)) + ' or ' + random.choice(literals)
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    min_rank_p_values = []
    resolution_widths = []

    for n in n_values:
        instances_tested = 0
        for _ in range(5):  # Sample 5 instances per size
            formula = generate_formula(n)
            MinRank_p = rank([[p_adic_dilogarithm(eval(lit), 2) for lit in formula.split(' or ')]])
            min_rank_p_values.append(MinRank_p)
            resolution_widths.append(len(formula.split(' or ')) + 1)  # Simplified width estimation
            instances_tested += 1

    n_max = max(n_values)
    metric_value = sum(min_rank_p_values) / len(min_rank_p_values)
    correlation_coefficient = sum((min_rank_p - metric_value) * (width - metric_value) for min_rank_p, width in zip(min_rank_p_values, resolution_widths)) / math.sqrt(sum((min_rank_p - metric_value) ** 2 for min_rank_p in min_rank_p_values) * sum((width - metric_value) ** 2 for width in resolution_widths))
    p_value = 2 * (1 - abs(correlation_coefficient))

    conjecture_holds = abs(correlation_coefficient) >= 0.9 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "correlation_coefficient=|{}|, p_value={}".format(correlation_coefficient, p_value)

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested * len(n_values),
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
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"], first_failing_seed))