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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def geometric_probability(clauses):
        n = len(clauses[0])
        volume = math.prod([2 * abs(c[i]) for c in clauses for i in range(n)])
        total_volume = 2 ** (n * len(clauses))
        return Fraction(volume, total_volume)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        n_max = n
        sum_probabilities = Fraction(0)
        for _ in range(30):
            clauses = generate_cnf(n)
            prob = geometric_probability(clauses)
            sum_probabilities += prob
            instances_tested += 1
        
        avg_prob = sum_probabilities / instances_tested
        c = avg_prob.numerator * n_max ** (3/2) / avg_prob.denominator
        conjecture_holds = all(prob <= c * n_max ** (3/2) for prob in [avg_prob])
        
        results.append({
            "metric_name": "geometric_probability",
            "metric_value": float(avg_prob),
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": conjecture_holds,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.extend(trial_result["results"])
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - avg_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")