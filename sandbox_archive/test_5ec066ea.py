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

def calculate_entropy(tensor_product):
    # Placeholder for actual entropy calculation using tensor products
    return sum(math.log2(1 / len(tensor_product)) for _ in tensor_product)

def generate_cnf(num_clauses, num_vars):
    cnf = []
    for _ in range(num_clauses):
        clause = [random.choice([i, -i]) for i in random.sample(range(1, num_vars + 1), random.randint(1, num_vars))]
        cnf.append(clause)
    return cnf

def run_dpll(cnf):
    def dpll():
        if not cnf:
            return True
        literal = next((lit for lit in range(1, len(cnf) + 1) if any(lit in clause for clause in cnf)), None)
        if literal is None:
            return False
        assignment[literal] = True
        new_cnf = [clause for clause in cnf if not all(lit in clause or -lit in clause for lit in assignment)]
        if dpll():
            return True
        del assignment[literal]
        assignment[-literal] = True
        new_cnf = [clause for clause in cnf if not all(lit in clause or -lit in clause for lit in assignment)]
        if dpll():
            return True
        del assignment[-literal]
        return False

    assignment = {}
    stack = []
    return len(stack) if dpll() else 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    entropies = []
    lengths = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, n)
            tensor_product = calculate_tensor_product(cnf)
            entropy = calculate_entropy(tensor_product)
            dpll_length = run_dpll(cnf)
            entropies.append(entropy)
            lengths.append(dpll_length)
    if len(entropies) < 30:
        return {
            "metric_name": "Geometric Entropy vs DPLL Proof Length",
            "metric_value": None,
            "instances_tested": len(entropies),
            "n_max": max(len(cnf) for cnf in [generate_cnf(n, n) for n in [5, 10, 15, 20, 30, 40]]),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    correlation_coefficient = calculate_correlation(entropies, lengths)
    p_value = calculate_p_value(correlation_coefficient, len(entropies))
    return {
        "metric_name": "Geometric Entropy vs DPLL Proof Length",
        "metric_value": correlation_coefficient,
        "instances_tested": len(entropies),
        "n_max": max(len(cnf) for cnf in [generate_cnf(n, n) for n in [5, 10, 15, 20, 30, 40]]),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": ""
    }

def calculate_correlation(x, y):
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x))) / len(x)
    std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(len(x))) / len(x))
    std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(len(y))) / len(y))
    return cov_xy / (std_dev_x * std_dev_y)

def calculate_p_value(r, n):
    t_statistic = r * math.sqrt((n - 2) / (1 - r**2))
    degrees_of_freedom = n - 2
    p_value = 2 * (1 - math.erf(abs(t_statistic) / math.sqrt(2)))
    return p_value

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None])
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None) / len([r for r in results if r['metric_value'] is not None]))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")