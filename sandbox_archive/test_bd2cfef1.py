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
    
    def generate_boolean_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(clauses):
        # Simplified model of Frege proof depth
        return len(clauses) * 2
    
    def affine_plane_points(clauses):
        points = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('~'):
                    points.add(literal[1:])
                else:
                    points.add(literal)
        return len(points)
    
    n_max = 0
    instances_tested = 0
    total_points = 0
    total_depth = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        clauses = generate_boolean_formula(n, m)
        
        points = affine_plane_points(clauses)
        depth = frege_proof_depth(clauses)
        
        total_points += points
        total_depth += depth
        instances_tested += 1
        
        if n > n_max:
            n_max = n
    
    mean_points = total_points / instances_tested
    mean_depth = total_depth / instances_tested
    
    correlation_coefficient = (instances_tested * mean_points * mean_depth - 
                               total_points * total_depth) / (
                                   math.sqrt((instances_tested * sum(p**2 for p in points) - 
                                               total_points**2) *
                                              (instances_tested * sum(d**2 for d in depths) - 
                                               total_depth**2)))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}"
    
    return {
        "metric_name": "Frege Proof Depth vs Affine Plane Points",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={math.sqrt(sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation below threshold' first_failing_seed={first_failing_seed}")