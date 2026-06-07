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
    
    def communication_complexity_rank_variance(cnf):
        # Placeholder implementation
        return random.random()
    
    def minimal_root_system_length(cnf):
        # Placeholder implementation
        return random.randint(1, 10)
    
    n = 5  # Start with small n and increase to 40
    instances_tested = 0
    total_L = 0
    total_w = 0
    
    while instances_tested < 30:
        cnf = generate_cnf(n)
        L = minimal_root_system_length(cnf)
        w = communication_complexity_rank_variance(cnf)
        
        if L is not None and w is not None:
            total_L += L
            total_w += w
            instances_tested += 1
        
        n += 5
    
    mean_L = total_L / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(L * w for L, w in zip([mean_L] * instances_tested, [mean_w] * instances_tested)) - 
                               sum(L for L in [mean_L] * instances_tested) * sum(w for w in [mean_w] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(L**2 for L in [mean_L] * instances_tested) - sum(L for L in [mean_L] * instances_tested)**2) *
                                        (instances_tested * sum(w**2 for w in [mean_w] * instances_tested) - sum(w for w in [mean_w] * instances_tested)**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n - 5,
        "conjecture_holds": 0.8 <= abs(correlation_coefficient) <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")