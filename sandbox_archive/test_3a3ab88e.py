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

def generate_group(n):
    if n == 1:
        return [0]
    elements = list(range(1, n))
    random.shuffle(elements)
    group = [0] + elements
    return group

def character_table(group):
    n = len(group)
    table = [[Fraction(1) for _ in range(n)] for _ in range(n)]
    for i in range(1, n):
        for j in range(i+1, n):
            if (group[i] * group[j]) % n == 1:
                table[i][j] = Fraction(-1)
                table[j][i] = Fraction(-1)
    return table

def min_representation_order(group):
    n = len(group)
    table = character_table(group)
    min_order = float('inf')
    for i in range(n):
        order = 0
        for j in range(n):
            if table[i][j] != 0:
                order += abs(table[i][j])
        min_order = min(min_order, order)
    return min_order

def generate_matrix_product_problem(group, representation):
    n = len(group)
    m = max(len(row) for row in representation)
    matrix_product = [[0 for _ in range(m)] for _ in range(m)]
    for g1 in group:
        for i in range(m):
            for j in range(m):
                product[i][j] += representation[g1][i][k] * representation[group[g1]][k][j]
    return matrix_product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    group = generate_group(n)
    representation = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    min_order = min_representation_order(group)
    matrix_product = generate_matrix_product_problem(group, representation)
    comm_rank = sum(1 for row in matrix_product if any(x != 0 for x in row))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": Fraction(min_order * comm_rank).limit_denominator(),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")