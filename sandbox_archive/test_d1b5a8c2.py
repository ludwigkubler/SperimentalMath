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

def generate_random_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
            clauses.append(clause)
    return clauses

def symplectic_quotient_order(clauses):
    n = len(clauses[0])
    vectors = [[Fraction(1 if abs(c[i]) == 1 else 0, abs(c[i])) for i in range(n)] for c in clauses]
    # Simplify vectors to canonical form
    for i in range(n):
        for j in range(i + 1, n):
            if vectors[i][j] != 0:
                scale = vectors[j][i] / vectors[i][i]
                for k in range(n):
                    vectors[j][k] -= scale * vectors[i][k]
    # Count non-zero entries
    return sum(sum(1 for v in row if v != 0) for row in vectors)

def resolution_proof_width(clauses):
    n = len(clauses[0])
    stack = []
    for clause in clauses:
        stack.append(clause)
    while stack:
        clause1 = stack.pop()
        if not any(any(abs(c1[i]) == abs(c2[i]) and c1[i] != c2[i] for i in range(n)) for c2 in stack):
            return len(stack) + 1
        clause2 = next(c2 for c2 in stack if any(abs(c1[i]) == abs(c2[i]) and c1[i] != c2[i] for i in range(n)))
        new_clause = [c1[i] * c2[i] for i in range(n)]
        stack.append(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_order = 0
        total_width = 0
        for _ in range(5):  # Sample 5 instances per size
            m = random.randint(n // 2, n)
            clauses = generate_random_cnf(n, m)
            order = symplectic_quotient_order(clauses)
            width = resolution_proof_width(clauses)
            total_order += order
            total_width += width
            instances_tested += 1
        avg_order = Fraction(total_order, instances_tested)
        avg_width = Fraction(total_width, instances_tested)
        results.append((avg_order, avg_width))
    n_max = max(n_values)
    metric_value = sum(order * width for order, width in results) / sum(width for _, width in results)
    conjecture_holds = all(0.5 <= abs(order * width - metric_value) <= 1 for order, width in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Correlation",
        "metric_value": float(metric_value),
        "instances_tested": sum(5 for _ in n_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")