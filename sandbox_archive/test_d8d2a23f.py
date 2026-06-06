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
    
    def generate_boolean_formula(m, n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' ∨ '.join(clause))
        return ' ∧ '.join(clauses)
    
    def count_points(formula):
        points = set()
        for term in formula.split():
            if term.startswith('~'):
                var = term[1:]
                points.add(var)
                points.add(f'~{var}')
            else:
                points.add(term)
                points.add(f'~{term}')
        return len(points) // 2
    
    def frege_proof_depth(formula):
        # Simplified estimation of Frege proof depth
        return len(formula.split(' ∧ ')) + len(formula.split(' ∨ '))
    
    instances_tested = 0
    points_sum = 0
    depths_sum = 0
    n_max = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            n = random.randint(1, min(m, 10))
            formula = generate_boolean_formula(m, n)
            points = count_points(formula)
            depth = frege_proof_depth(formula)
            
            instances_tested += 1
            points_sum += points
            depths_sum += depth
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "Frege Proof Depth vs Points",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_points = points_sum / instances_tested
    mean_depths = depths_sum / instances_tested
    correlation_coefficient = (instances_tested * sum((points - mean_points) * (depth - mean_depths) for points, depth in zip(points_list, depths_list)) -
                               sum(points - mean_points) * sum(depth - mean_depths)) / math.sqrt(instances_tested * sum((points - mean_points)**2 for points in points_list) *
                                                                                           instances_tested * sum((depth - mean_depths)**2 for depth in depths_list))
    
    return {
        "metric_name": "Frege Proof Depth vs Points",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.5 < correlation_coefficient < 0.7,
        "counterexample": "" if 0.5 < correlation_coefficient < 0.7 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")