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
    pass

def generate_cnf(num_clauses, num_vars):
    # Placeholder for CNF generation
    cnf = []
    for _ in range(num_clauses):
        clause = [random.choice([-1, 1]) * random.randint(1, num_vars) for _ in range(random.randint(2, num_vars + 1))]
        cnf.append(clause)
    return cnf

def calculate_tensor_product(cnf):
    # Placeholder for tensor product calculation
    tensor_product = []
    for clause in cnf:
        new_clause = [random.choice([-1, 1]) * literal for literal in clause]
        tensor_product.extend(new_clause)
    return tensor_product

def run_dpll(cnf):
    # Placeholder for DPLL algorithm
    assignment = {}
    stack = [(cnf, assignment)]
    while stack:
        cnf, assignment = stack.pop()
        if not cnf:
            return 1
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            stack.append(([(l for l in c if l != literal and l != -literal) for c in cnf], new_assignment))
            continue
        literal, _ = random.choice(cnf)
        new_assignment1 = assignment.copy()
        new_assignment1[literal] = True
        stack.append(([c for c in cnf if literal not in c and -literal not in c], new_assignment1))
        new_assignment2 = assignment.copy()
        new_assignment2[literal] = False
        stack.append(([c for c in cnf if -literal not in c and literal not in c], new_assignment2))
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    entropies = []
    lengths = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, n * 2)
            cnf = generate_cnf(m, n)
            tensor_product = calculate_tensor_product(cnf)
            entropy = calculate_entropy(tensor_product)
            dpll_length = run_dpll(cnf)
            entropies.append(entropy)
            lengths.append(dpll_length)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(entropies, lengths)) / (len(entropies) * std_x * std_y)
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(entropies) - 3)))
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(entropies),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value <= 0.05,
        "counterexample": "" if correlation_coefficient >= 0.7 and p_value <= 0.05 else "correlation_coefficient < 0.7 or p_value > 0.05"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_x = sum(r["metric_value"] for r in results) / len(results)
    std_x = math.sqrt(sum((r["metric_value"] - mean_x) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_x} std={std_x} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")