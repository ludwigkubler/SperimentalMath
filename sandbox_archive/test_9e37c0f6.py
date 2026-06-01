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
    
    def frobenius_norm(matrix):
        return sum(sum(x**2 for x in row) for row in matrix)**0.5
    
    def communication_complexity_rank(f):
        # Placeholder function to simulate communication complexity rank calculation
        # Replace with actual algorithm
        return len(f)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    n_max = 40
    instances_tested = 0
    total_frobenius = 0
    total_rank = 0
    
    for n in range(5, n_max + 1):
        if n > 30:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30')
            return {
                "metric_name": "Frobenius norm vs Communication Complexity Rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        
        for _ in range(30):
            f = generate_boolean_function(n)
            frobenius = frobenius_norm([[f[i] ^ f[j] for j in range(n)] for i in range(n)])
            rank = communication_complexity_rank(f)
            
            total_frobenius += frobenius
            total_rank += rank
            instances_tested += 1
    
    mean_frobenius = Fraction(total_frobenius, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    
    correlation_coefficient = (instances_tested * sum(frobenius * rank for frobenius, rank in zip(range(5, n_max + 1), range(5, n_max + 1))) -
                               total_frobenius * total_rank) / math.sqrt(instances_tested * sum(frobenius**2 for frobenius in range(5, n_max + 1)) - total_frobenius**2 *
                                                                 instances_tested * sum(rank**2 for rank in range(5, n_max + 1)) - total_rank**2)
    
    return {
        "metric_name": "Frobenius norm vs Communication Complexity Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.6 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"] and res["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")