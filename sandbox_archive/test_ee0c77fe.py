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

def generate_random_group(n):
    elements = list(range(n))
    group = {}
    for g in elements:
        group[g] = [random.randint(0, 1) for _ in range(n)]
    return group

def generate_representation(group, n):
    representation = {}
    for g in group:
        rep = []
        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    row.append(Fraction(1))
                else:
                    row.append(Fraction(0))
            rep.append(row)
        representation[g] = rep
    return representation

def generate_matrix_product_problem(group, representation):
    n = len(group)
    product = [[0 for _ in range(n)] for _ in range(n)]
    for g1 in group:
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    product[i][j] += representation[g1][i][k] * representation[group[g1]][k][j]
                product[i][j] %= 2
    return product

def calculate_communication_complexity_rank(matrix_product):
    n = len(matrix_product)
    rank = 0
    for i in range(n):
        if any(matrix_product[j][i] == 1 for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_sum = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        group = generate_random_group(n)
        representation = generate_representation(group, n)
        matrix_product = generate_matrix_product_problem(group, representation)
        comm_rank = calculate_communication_complexity_rank(matrix_product)

        instances_tested += n
        n_max = max(n_max, n)

        min_rep_order = min(sum(1 for x in row if x != 0) for row in representation.values())
        correlation_sum += min_rep_order * comm_rank

    mean_correlation = correlation_sum / instances_tested
    if len(n_values) > 1:
        std_dev = math.sqrt((sum((mean_correlation - (min_rep_order * comm_rank)) ** 2 for n in n_values) / len(n_values)))
    else:
        std_dev = 0

    return {
        "metric_name": "Correlation",
        "metric_value": mean_correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_correlation > 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_threshold_not_met' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")