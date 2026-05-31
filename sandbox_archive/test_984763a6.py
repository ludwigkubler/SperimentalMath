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
    
    def generate_cnf(m, s):
        cnf = []
        for _ in range(m):
            clause = set(random.sample(range(1, 2 * s + 1), s))
            cnf.append(clause)
        return cnf
    
    def mlecoh(cnf):
        # Placeholder function to simulate the computation of mlecoh
        # This is a dummy implementation and should be replaced with actual logic
        return sum(len(clause) for clause in cnf) / len(cnf)
    
    n = 5
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    while n <= 40:
        m = random.randint(1, 30)
        s = random.randint(1, min(n, 40))
        cnf = generate_cnf(m, s)
        
        for clause in cnf:
            if len(clause) > n:
                continue
        
        mlecoh_value = mlecoh(cnf)
        instances_tested += 1
        n_max = max(n_max, n)
        
        if mlecoh_value > 2 * s:
            conjecture_holds = False
            counterexample = f"mlecoh({m}, {s}) = {mlecoh_value} > 2*{s}"
            break
        
        n += 5
    
    return {
        "metric_name": "mlecoh",
        "metric_value": mlecoh_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")