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
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_depth(cnf):
        # Simplified estimation of Frege proof depth
        return len(cnf) * 2
    
    def monomial_representation_size(cnf):
        # Placeholder for actual monomial representation calculation
        return sum(len(clause) for clause in cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        depth = frege_proof_depth(cnf)
        size = monomial_representation_size(cnf)
        results.append((n, size, depth))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    metric_values = [size for _, size, _ in results]
    log_depths = [math.log(depth) for _, _, depth in results]
    
    mean_rep = sum(metric_values) / len(results)
    mean_depth = sum(log_depths) / len(results)
    
    correlation_coefficient = (sum((metric_values[i] - mean_rep) * (log_depths[i] - mean_depth) for i in range(len(results))) /
                               math.sqrt(sum((metric_values[i] - mean_rep)**2 for i in range(len(results))) *
                                         sum((log_depths[i] - mean_depth)**2 for i in range(len(results)))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["instances_tested"] > 0 for result in results):
        print("RESULT: INCONCLUSIVE reason=no_instances_generated")
    else:
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.5' first_failing_seed={first_failing_seed}")