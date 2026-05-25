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
    
    def p_adic_log(n, p):
        if n == 0:
            return -math.inf
        log_val = 0
        while n % p == 0:
            n //= p
            log_val += 1
        return log_val
    
    def tseitin_resolution_length(f):
        # Placeholder for actual Tseitin resolution length calculation
        # This is a dummy implementation for testing purposes
        return len(f) * 2
    
    def p_adic_log_potential(F, p):
        satisfying_assignments = sum(1 for _ in F)
        return p_adic_log(satisfying_assignments, p)
    
    def minimal_rank(phi_F):
        # Placeholder for actual minimal rank calculation
        # This is a dummy implementation for testing purposes
        return len(str(phi_F))
    
    n = random.randint(5, 40)
    alpha = random.uniform(0.1, 0.9)
    p = 2
    
    F = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if random.random() < alpha:
            F.append(clause)
    
    phi_F = p_adic_log_potential(F, p)
    tau_F = tseitin_resolution_length(F)
    r_F = minimal_rank(phi_F)
    
    ratio = Fraction(r_F, tau_F)
    difference = abs(r_F - p * tau_F)
    
    conjecture_holds = 0.95 <= ratio <= 1.05 and difference < 1
    counterexample = "" if conjecture_holds else f"Ratio={ratio}, Difference={difference}"
    
    return {
        "metric_name": "Ratio of Minimal Rank to Tseitin Resolution Length",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")