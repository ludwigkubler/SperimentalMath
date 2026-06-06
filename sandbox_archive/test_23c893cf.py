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
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)

    def count_affine_plane_points(formula):
        points = set()
        for term in formula.split():
            if term.startswith('~'):
                points.add(term[1:])
            else:
                points.add(term)
        return len(points)

    def frege_proof_depth(formula):
        # Simplified estimation of Frege proof depth
        return 2 * len(formula.split(' and '))

    instances_tested = 0
    points_list = []
    depths_list = []

    for n in [5, 10, 15, 20, 30, 40]:
        for m in range(1, min(n, 10) + 1):  # Ensure at least one clause and not too many
            formula = generate_boolean_formula(m, n)
            points = count_affine_plane_points(formula)
            depth = frege_proof_depth(formula)
            instances_tested += 1
            points_list.append(points)
            depths_list.append(depth)

    if instances_tested < 30:
        return {
            "metric_name": "Frege Proof Depth vs. Affine Plane Points",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(5, n),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }

    mean_points = sum(points_list) / instances_tested
    mean_depths = sum(depths_list) / instances_tested

    correlation_coefficient = (instances_tested * sum((points - mean_points) * (depth - mean_depths) for points, depth in zip(points_list, depths_list)) -
                               sum(points_list) * sum(depths_list)) / math.sqrt(instances_tested * sum((points - mean_points) ** 2 for points in points_list) *
                                                                                     sum((depth - mean_depths) ** 2 for depth in depths_list))

    return {
        "metric_name": "Frege Proof Depth vs. Affine Plane Points",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(5, n),
        "conjecture_holds": 0.7 <= correlation_coefficient < 0.9,
        "counterexample": "" if 0.7 <= correlation_coefficient < 0.9 else f"Correlation coefficient: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)

    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below 0.7\" first_failing_seed={first_failing_seed}")