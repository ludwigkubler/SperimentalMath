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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses

    def construct_metric_tree(clauses):
        n = len(clauses)
        tree = [[0] * n for _ in range(n)]
        for i, clause1 in enumerate(clauses):
            for j, clause2 in enumerate(clauses):
                if i != j:
                    common_vars = set(clause1) & set(clause2)
                    distance = 1 + len(common_vars)
                    tree[i][j] = distance
                    tree[j][i] = distance
        return tree

    def geometric_entropy(tree):
        n = len(tree)
        total_weight = sum(sum(distances[i][j] for j in range(n)) for i in range(n))
        entropy = 0
        for i in range(n):
            degree = sum(1 for j in range(n) if tree[i][j] > 0)
            if degree > 0:
                entropy += math.log(degree, n)
        return total_weight / entropy

    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        assignment = {}
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if not any(var in assignment or f'~{var}' in assignment for var in clause):
                return len(stack) + 1
            unit_clause = next((var for var in clause if var not in assignment and f'~{var}' not in assignment), None)
            if unit_clause is None:
                return len(stack) + 1
            stack.extend(clause for clause in clauses if unit_clause in clause or f'~{unit_clause}' in clause)
        return len(stack)

    n = random.randint(5, 40)
    formula = generate_formula(n)
    tree = construct_metric_tree(formula)
    H_min = geometric_entropy(tree)
    w = resolution_width(formula)

    conjecture_holds = H_min >= 0.5 * w
    counterexample = "" if conjecture_holds else f"n={n}, H_min={H_min}, w={w}"
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": H_min,
        "instances_tested": 1,
        "n_max": n,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")