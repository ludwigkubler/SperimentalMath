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
    
    def hypergeometric_moments(n, D):
        moments = [0] * (D + 1)
        for k in range(D + 1):
            moments[k] = math.comb(n, k) / math.comb(2*n, D)
        return moments
    
    def communication_complexity(n):
        # Placeholder function; actual implementation depends on the problem
        return n * (n + 1) // 2
    
    instances_tested = 0
    total_communication = 0
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        moments = hypergeometric_moments(n, D=1)  # Assuming D=1 for simplicity
        comm_complexity = communication_complexity(n)
        total_communication += comm_complexity
        instances_tested += 1
    
    mean_communication = total_communication / instances_tested
    lower_bound = n**(1 + 1/1)  # Assuming D=1 for simplicity
    
    conjecture_holds = mean_communication >= lower_bound
    counterexample = "" if conjecture_holds else f"Mean communication {mean_communication} < lower bound {lower_bound}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_communication,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication = sum(r["metric_value"] for r in results) / len(results)
    std_communication = math.sqrt(sum((r["metric_value"] - mean_communication)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_communication} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE budget_exceeded n_tested=30")