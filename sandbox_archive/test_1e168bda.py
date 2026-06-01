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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            clauses.append(clause)
        return clauses
    
    def geometric_entropy(clauses):
        counts = {}
        for clause in clauses:
            for literal in clause:
                if literal not in counts:
                    counts[literal] = 0
                counts[literal] += 1
        entropy = 0
        total = sum(counts.values())
        for count in counts.values():
            p = Fraction(count, total)
            entropy -= p * math.log2(p)
        return entropy
    
    def clause_set_complexity(clauses):
        return len(set(tuple(sorted(clause)) for clause in clauses))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m_values = [n + i for i in range(1, min(n + 6, 31))]
        for m in m_values:
            clauses = generate_cnf(n, m)
            mge = geometric_entropy(clauses)
            c_phi = clause_set_complexity(clauses)
            results.append({"n": n, "m": m, "mge": mge, "c_phi": c_phi})
    
    if not results:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    instances_tested = len(results)
    
    mge_values = [result["mge"] for result in results]
    c_phi_values = [result["c_phi"] for result in results]
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    slope, intercept, r_squared = linear_regression(c_phi_values, mge_values)
    
    conjecture_holds = r_squared >= 0.7
    counterexample = "" if conjecture_holds else "r_squared < 0.7"
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": slope,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        sys.exit(0)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = f"r_squared < 0.7 at seed {first_failing_seed}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")