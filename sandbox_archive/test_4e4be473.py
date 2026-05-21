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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(3 * n):
            literals = [random.randint(0, 1) for _ in range(n)]
            clause = tuple(literals)
            clauses.append(clause)
        return clauses
    
    def discrepancy(clauses):
        n = len(clauses[0])
        disc = 0
        for x in range(2**n):
            if all(x & (1 << i) == y & (1 << i) or (x & (1 << i)) * (y & (1 << i)) >= 0 for clause, y in zip(clauses, range(2**n))):
                disc += 1
        return disc
    
    def integrate_discrepancy(n, disc):
        # Discretize the unit sphere and approximate the integral
        num_points = 1000
        points = []
        for _ in range(num_points):
            point = [random.uniform(-1, 1) for _ in range(n)]
            norm = sum(x**2 for x in point)
            if norm > 0:
                point = [x / math.sqrt(norm) for x in point]
                points.append(point)
        
        volume_sum = 0
        for point in points:
            product_of_halfspaces = 1
            for i, literal in enumerate(clauses[0]):
                if literal == 1:
                    product_of_halfspaces *= max(0, point[i])
                else:
                    product_of_halfspaces *= max(0, -point[i])
            volume_sum += product_of_halfspaces
        
        return (volume_sum / num_points) * math.pow(math.pi, n-1)
    
    n = 40
    clauses = generate_3cnf(n)
    disc = discrepancy(clauses)
    integral_approximation = integrate_discrepancy(n, disc)
    
    metric_name = "discrepancy_communication_complexity"
    metric_value = abs(disc - integral_approximation)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")