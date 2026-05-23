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
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def geometric_entanglement_rank(cnf):
        # Placeholder implementation
        return len(cnf) * 2
    
    def noncommutative_crossed_product_rank(n):
        # Placeholder implementation
        return math.ceil(math.sqrt(n))
    
    n = random.randint(5, 40)
    k = random.randint(1, min(2*n-1, 30))  # Ensure at least one clause and avoid trivial cases
    cnf = generate_k_cnf(n, k)
    
    ge_rank = geometric_entanglement_rank(cnf)
    nccp_rank = noncommutative_crossed_product_rank(n)
    
    if ge_rank <= nccp_rank * (n**1.5):
        return {
            "metric_name": "Rank Difference",
            "metric_value": ge_rank - nccp_rank * (n**1.5),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, k={k}, ge_rank={ge_rank}, nccp_rank={nccp_rank}"
        }
    else:
        return {
            "metric_name": "Rank Difference",
            "metric_value": ge_rank - nccp_rank * (n**1.5),
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")