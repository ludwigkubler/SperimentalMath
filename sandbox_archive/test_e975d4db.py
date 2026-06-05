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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def generate_group(n):
    if n == 2:
        return {0: [1], 1: [0]}
    elif n == 3:
        return {0: [1, 2], 1: [2, 0], 2: [0, 1]}
    else:
        raise ValueError("Unsupported group size")

def character_table(group):
    n = len(group)
    table = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if group[i][j] == i:
                table[i][j] = 1
    return table

def min_representation_order(group):
    char_table = character_table(group)
    n = len(char_table)
    order = float('inf')
    for row in char_table:
        for val in row:
            if val != 0:
                order = min(order, abs(val))
    return order

def generate_matrix_product_problem(group, representation):
    n = len(group)
    matrix_product = [[0] * n for _ in range(n)]
    for g1 in group:
        for i in range(n):
            for j in range(n):
                product[i][j] += representation[g1][i][k] * representation[group[g1]][k][j]
    return matrix_product

def comm_complexity_rank(matrix_product):
    n = len(matrix_product)
    rank = 0
    for i in range(n):
        for j in range(n):
            if matrix_product[i][j] != 0:
                rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            continue
        
        group = generate_group(n)
        representation = character_table(group)
        min_order = min_representation_order(group)
        matrix_product = generate_matrix_product_problem(group, representation)
        comm_rank = comm_complexity_rank(matrix_product)
        
        instances_tested += 1
        total_metric_value += abs(min_order - comm_rank)
    
    if instances_tested == 0:
        return {
            "metric_name": "abs_diff",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "abs_diff",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_metric_value < 1.0,  # Simplified for testing purposes
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")