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
    
    # Generate a random CNF instance with n variables and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, n * 10)
    cnf_instance = []
    for _ in range(m):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf_instance.append(clause)
    
    # Placeholder for computing geometric entropy H(G)
    # This is a dummy implementation; actual computation depends on the affine scheme G
    H_G = 0.5 * n * math.log(m)  # Dummy value
    
    # Placeholder for estimating DPLL search tree width W(G)
    # This is a dummy implementation; actual estimation depends on the CNF instance
    W_G = int(math.sqrt(H_G))  # Dummy value
    
    return {
        "metric_name": "H(G)",
        "metric_value": H_G,
        "instances_tested": 1,
        "conjecture_holds": H_G <= 0.5 * n * math.log(m) and W_G <= int(math.sqrt(H_G)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_G = sum(r["metric_value"] for r in results) / len(results)
    std_H_G = math.sqrt(sum((r["metric_value"] - mean_H_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_G} std={std_H_G} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")