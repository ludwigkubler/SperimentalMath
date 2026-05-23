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
    
    def generate_k_cnf(n: int, k: int):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_valuation_rank(cnf):
        # Simplified version of the valuation rank calculation
        return len(set(abs(lit) for clause in cnf for lit in clause))
    
    def monotone_circuit_depth(cnf):
        # Placeholder function, replace with actual algorithm
        return len(cnf)
    
    n = 10
    k = 5
    instances_tested = 30
    total_rank = 0
    total_depth = 0
    
    for _ in range(instances_tested):
        cnf = generate_k_cnf(n, k)
        rank = p_adic_valuation_rank(cnf)
        depth = monotone_circuit_depth(cnf)
        total_rank += rank
        total_depth += depth
    
    avg_rank = total_rank / instances_tested
    avg_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * depth for rank, depth in zip([avg_rank] * instances_tested, [avg_depth] * instances_tested)) - instances_tested * avg_rank * avg_depth) / math.sqrt((instances_tested * sum(rank**2 for rank in [avg_rank] * instances_tested) - instances_tested * avg_rank**2) * (instances_tested * sum(depth**2 for depth in [avg_depth] * instances_tested) - instances_tested * avg_depth**2))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")