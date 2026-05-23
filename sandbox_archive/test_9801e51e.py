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
    
    def generate_k_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            cnf.append(clause)
        return cnf
    
    def tropicalized_cohomology(cnf):
        # Placeholder function to simulate the computation
        cohomology = {}
        max_var = 0
        for clause in cnf:
            for var in clause:
                if var > max_var:
                    max_var = var
                if var not in cohomology or len(clause) > len(cohomology[var]):
                    cohomology[var] = len(clause)
        return cohomology, max_var
    
    def minimal_rank(cohomology):
        return sum(len(v) for v in cohomology.values())
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        total_rank = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_k_cnf(n, random.randint(1, n))
            cohomology, max_var = tropicalized_cohomology(cnf)
            rank = minimal_rank(cohomology)
            total_rank += rank
        
        avg_rank = total_rank / len(n_values)
        results.append(avg_rank)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(rank <= 3 * (metric_value - median) for rank in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 3 * (mean - median)) / len(results)
    
    if all(r <= 3 * (mean - median) for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 3 * (mean - median) for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result > 3 * (mean - median))
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")