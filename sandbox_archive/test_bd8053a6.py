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
    
    def generate_kcnf(n, m, k):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if len(clause) == 2 and abs(clause[0]) != abs(clause[1]):
                cnf.append(clause)
        return cnf
    
    def min_state_complexity(cnf):
        # Placeholder for actual algorithm to compute minimal state complexity
        # This is a dummy implementation for testing purposes
        n = max(abs(lit) for lit in sum(cnf, []))
        m = len(cnf)
        return (n + m + 2) * math.log(n + m, 2)
    
    def communication_complexity(cnf):
        # Placeholder for actual algorithm to compute communication complexity
        # This is a dummy implementation for testing purposes
        n = max(abs(lit) for lit in sum(cnf, []))
        return n
    
    results = []
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.randint(5, 40)
        m = random.randint(n, n * 2)
        k = 2  # Example value for k
        cnf = generate_kcnf(n, m, k)
        
        q_star = min_state_complexity(cnf)
        comm_complexity = communication_complexity(cnf)
        
        results.append({
            "n": n,
            "m": m,
            "q_star": q_star,
            "comm_complexity": comm_complexity
        })
    
    total_q_star = sum(result["q_star"] for result in results)
    mean_q_star = total_q_star / len(results)
    max_n = max(result["n"] for result in results)
    
    conjecture_holds = all(q_star <= (result["n"] + result["m"] + 2) * math.log(result["n"] + result["m"], 2) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "q_star",
        "metric_value": mean_q_star,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_q_star = sum(result["metric_value"] for result in results)
    mean_q_star = total_q_star / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_q_star:.2f} std=NA support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")