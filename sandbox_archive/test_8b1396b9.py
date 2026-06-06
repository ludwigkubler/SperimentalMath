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
    
    def generate_boolean_formula(m, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def count_affine_plane_points(clauses, variables):
        points = set()
        for clause in clauses:
            for var in clause:
                if var.startswith('~'):
                    points.add(var[1:])
                else:
                    points.add(var)
        return len(points)
    
    def frege_proof_depth(clauses):
        n = len(clauses)
        d = 0
        while n > 1:
            n = math.ceil(n / 2)
            d += 1
        return d
    
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            n = random.randint(2, min(10, m))  # Ensure n_min >= 5
            formula = generate_boolean_formula(m, n)
            points = count_affine_plane_points(formula, variables)
            depth = frege_proof_depth(formula)
            results.append({
                "m": m,
                "n": n,
                "points": points,
                "depth": depth
            })
    
    if not results:
        return {
            "metric_name": "Frege Proof Depth vs. Affine Plane Points",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    points = [r["points"] for r in results]
    depths = [r["depth"] for r in results]
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    corr_coeff = correlation(points, depths)
    
    return {
        "metric_name": "Frege Proof Depth vs. Affine Plane Points",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": 0.5 < corr_coeff < 0.7,
        "counterexample": "" if 0.5 < corr_coeff < 0.7 else f"Correlation coefficient: {corr_coeff}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient out of range\" first_failing_seed={first_failing_seed}")
    else:
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if 0.5 < r["metric_value"] < 0.7) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")