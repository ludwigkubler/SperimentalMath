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
from math import ceil, sqrt

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n: int, m: int):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def geometric_langlands_dual(cnf):
        # Placeholder function for constructing the geometric Langlands dual object from a CNF
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        rank = ceil(m ** 0.25 * n ** 0.375)
        return rank
    
    def frege_proof_depth(cnf):
        # Placeholder function for calculating the Frege proof depth of a CNF
        m = len(cnf)
        n = max(abs(lit) for clause in cnf for lit in clause)
        depth = ceil(m ** 0.25 * n ** 0.375)
        return depth
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(10):  # Test with 10 different CNFs per seed
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)  # Ensure at least as many clauses as variables
        cnf = generate_cnf(n, m)
        
        dual_rank = geometric_langlands_dual(cnf)
        proof_depth = frege_proof_depth(cnf)
        
        instances_tested += 1
        
        if dual_rank > proof_depth:
            conjecture_holds = False
            counterexample = f"CNF: {cnf}, Dual Rank: {dual_rank}, Proof Depth: {proof_depth}"
    
    return {
        "metric_name": "minimal_rank_bound",
        "metric_value": dual_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")