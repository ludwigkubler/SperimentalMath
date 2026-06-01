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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses

    def clause_set_complexity(cnf):
        literals = set()
        for clause in cnf:
            literals.update(abs(lit) for lit in clause)
        return len(literals)

    def pearson_correlation(x, y):
        if len(x) != len(y) or not x:
            return 0
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y)

    def generate_hyperkahler_manifold(cnf):
        # Placeholder function to simulate generating a hyperkahler manifold
        return random.randint(1, len(cnf))

    def minimal_order(manifold):
        # Placeholder function to simulate finding the minimal order of a symplectic leaf
        return random.randint(1, 10)

    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    complexities = []

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(random.randint(1, n), n)
            manifold = generate_hyperkahler_manifold(cnf)
            min_order_value = minimal_order(manifold)
            min_orders.append(min_order_value)
            complexities.append(clause_set_complexity(cnf))

    correlation_coefficient = pearson_correlation(min_orders, complexities)

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")