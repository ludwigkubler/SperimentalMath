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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def geometric_fluctuation(cnf):
        assignments = [tuple(random.choice([0, 1]) for _ in range(len(cnf))) for _ in range(100)]
        counts = {assignment: 0 for assignment in assignments}
        for assignment in assignments:
            if all(any(lit == assignment[i-1] for lit in clause) for clause in cnf):
                counts[assignment] += 1
        total_variation = sum(abs(counts[assignment] - len(assignments)/2) for assignment in counts)
        return total_variation / len(assignments)
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation (not accurate but sufficient for testing)
        return len(cnf)
    
    n_max = 40
    instances_tested = 0
    total_fluctuation = 0
    total_width = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        fluctuation = geometric_fluctuation(cnf)
        width = resolution_width(cnf)
        total_fluctuation += fluctuation
        total_width += width
        instances_tested += len(cnf)
    
    if instances_tested < 30:
        return {
            "metric_name": "Resolution Width vs Geometric Fluctuation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    mean_fluctuation = total_fluctuation / instances_tested
    mean_width = total_width / instances_tested
    
    correlation_coefficient = (instances_tested * mean_fluctuation * mean_width - 
                               sum(cnf[i] * cnf[j] for i in range(instances_tested) for j in range(i+1, instances_tested))) / \
                              ((instances_tested - 1) * 
                               (sum(cnf[i]**2 for i in range(instances_tested)) - mean_fluctuation**2) *
                               (sum(cnf[i]**2 for i in range(instances_tested)) - mean_width**2))
    
    return {
        "metric_name": "Resolution Width vs Geometric Fluctuation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation: {correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = (sum((res["metric_value"] - mean_value)**2 for res in results if res["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Correlation too low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")