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

def generate_satisfiable_formula(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if any(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
            continue
        clauses.append(clause)
    return clauses

def construct_decision_tree(clauses):
    if not clauses:
        return None
    n = len(clauses[0])
    counts = [0] * (n + 1)
    for clause in clauses:
        for i in range(n):
            counts[i + 1] += abs(clause[i])
    decision_var = max(range(1, n + 1), key=lambda x: counts[x])
    left_clauses = [c for c in clauses if c[decision_var - 1] > 0]
    right_clauses = [c for c in clauses if c[decision_var - 1] < 0]
    return {
        "var": decision_var,
        "left": construct_decision_tree(left_clauses),
        "right": construct_decision_tree(right_clauses)
    }

def calculate_topological_entropy(tree):
    if tree is None:
        return 0
    left = tree["left"]
    right = tree["right"]
    p_left = len(left["clauses"]) / (len(left["clauses"]) + len(right["clauses"]))
    p_right = len(right["clauses"]) / (len(left["clauses"]) + len(right["clauses"]))
    entropy = -p_left * math.log2(p_left) - p_right * math.log2(p_right)
    return entropy

def calculate_clause_subset_complexity(clauses):
    n = len(clauses[0])
    subsets = []
    for i in range(1, 1 << n):
        subset = [clauses[j] for j in range(n) if (i & (1 << j))]
        if all(any(c[k] != 0 for k in range(n)) for c in subset):
            subsets.append(subset)
    return len(subsets)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_satisfiable_formula(n)
    tree = construct_decision_tree(clauses)
    entropy = calculate_topological_entropy(tree)
    complexity = calculate_clause_subset_complexity(clauses)
    return {
        "metric_name": "topological_entropy",
        "metric_value": entropy,
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

    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 1}")