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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_geometric_entropy(G_f):
    n = len(G_f)
    if n == 0:
        return 0.0
    total_weight = sum(len(neighbors) for neighbors in G_f.values())
    entropy = 0.0
    for neighbors in G_f.values():
        p = Fraction(len(neighbors), total_weight)
        entropy -= p * math.log2(p)
    return entropy

def compute_resolution_width(f):
    n = len(f)
    clauses = []
    for i in range(n):
        clauses.append([i, -i-1])
    model = {}
    def dpll(model, clauses):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause is None:
            return False
        p = random.choice(unit_clause)
        new_clauses = []
        for clause in clauses:
            if p not in clause and -p not in clause:
                new_clauses.append(clause)
        model[p] = True
        if dpll(model, new_clauses):
            return True
        del model[p]
        model[-p] = True
        if dpll(model, new_clauses):
            return True
        del model[-p]
        return False
    width = 0
    for i in range(2**n):
        current_model = {j: bool((i >> j) & 1) for j in range(n)}
        if not dpll(current_model, clauses):
            width += 1
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_width = 0.0
        total_entropy = 0.0
        for _ in range(5):
            f = generate_boolean_function(n)
            G_f = {}
            for i, val in enumerate(f):
                if val == 1:
                    neighbors = [j for j in range(n) if f[j] == 0]
                    G_f[i] = neighbors
            width = compute_resolution_width(f)
            entropy = compute_geometric_entropy(G_f)
            total_width += width
            total_entropy += entropy
            instances_tested += 1
        avg_width = total_width / instances_tested
        avg_entropy = total_entropy / instances_tested
        results.append((avg_width, avg_entropy))
    correlation_coefficient = sum((w - avg_w) * (h - avg_h) for w, h in results) / len(results)
    avg_w, avg_h = zip(*results)
    avg_w = sum(avg_w) / len(avg_w)
    avg_h = sum(avg_h) / len(avg_h)
    if correlation_coefficient >= 0.8:
        conjecture_holds = True
        counterexample = ""
    elif correlation_coefficient < 0.2:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    else:
        conjecture_holds = False
        counterexample = "non_linear_correlation"
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results) * 5,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < 0.2 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < 0.2))]
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")