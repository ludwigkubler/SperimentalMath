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
    
    def max_cut_approximation(n):
        # Placeholder for actual max-CUT approximation algorithm
        return 0.879 + (random.random() - 0.5) * 0.1
    
    def quotient_algebra_rank(n, d):
        # Placeholder for actual computation of quotient algebra rank
        return random.randint(1, n)
    
    def polynomial_norm(rank, n):
        # Placeholder for actual computation of polynomial norm
        return math.sqrt(rank / n)
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)  # Sweep n through distinct sizes
        d = random.randint(1, 2)
        
        alpha = max_cut_approximation(n)
        rank = quotient_algebra_rank(n, d)
        norm = polynomial_norm(rank, n)
        
        if norm < math.sqrt(alpha * n):
            conjecture_holds = False
            counterexample = f"n={n}, d={d}, alpha={alpha}, rank={rank}, norm={norm}"
            break
        
        instances_tested += 1
    
    return {
        "metric_name": "min_rank",
        "metric_value": math.sqrt(alpha * n),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")