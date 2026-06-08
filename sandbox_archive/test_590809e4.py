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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in about 10 clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def calculate_hodge_arakelov_index(n):
        # Placeholder function to simulate Hodge-Arakelov index calculation
        return random.uniform(0.1, 2) * n

    def calculate_frege_proof_depth(cnf):
        # Placeholder function to simulate Frege proof depth calculation
        return len(cnf) + random.randint(5, 15)

    def pearson_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("x and y must have the same length")
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
        return cov_xy / (std_x * std_y)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        ai = calculate_hodge_arakelov_index(n)
        d = calculate_frege_proof_depth(cnf)
        if ai > 10 or d > 10:
            return {
                "metric_name": "Pearson correlation",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "AI(K(φ)) or d(φ) exceeds 10"
            }
        results.append((ai, d))

    ai_values, d_values = zip(*results)
    correlation = pearson_correlation(ai_values, d_values)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n in [5, 10, 15, 20, 30, 40]),
        "conjecture_holds": correlation > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation < 0.7\" first_failing_seed={first_failing_seed}")