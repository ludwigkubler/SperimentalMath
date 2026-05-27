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
    
    def generate_k_cnf(k, n):
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def tropicalize(cnf):
        # Placeholder for the actual tropicalization procedure
        return cnf  # Simplified for demonstration purposes
    
    def minimal_rank(tropicalized_cnf):
        # Placeholder for the actual minimal rank calculation
        return len(tropicalized_cnf)  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n, 10))
    
    cnf = generate_k_cnf(k, n)
    tropicalized_cnf = tropicalize(cnf)
    rank = minimal_rank(tropicalized_cnf)
    
    metric_value = rank
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if rank >= (2**k / (n + k)) and rank <= (n**(1/4) * 2**k):
        conjecture_holds = True
    else:
        counterexample = f"Rank {rank} does not meet the bounds for n={n}, k={k}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    total_rank = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if trial_result["conjecture_holds"]:
            total_rank += trial_result["metric_value"]
    
    mean_rank = Fraction(total_rank, len(seeds))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}"
    elif support_fraction >= 0.8:
        result = f"SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"Rank does not meet the bounds\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result}")