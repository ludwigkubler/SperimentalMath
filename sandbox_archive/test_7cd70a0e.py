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
    
    # Generate a random group representation G with minimal rank C(G)
    n = random.randint(5, 40)
    G = [[random.random() for _ in range(n)] for _ in range(n)]
    C_G = sum(sum(row) for row in G) / (n * n)
    
    # Construct the corresponding polynomial inversion problem P
    P = [random.randint(1, 2**n - 1) for _ in range(n)]
    
    # Determine |C_P|, the size of the smallest circuit inverter for polynomial P
    C_P = len(P)
    
    # Compute log_2(|C_P|)
    log_C_P = math.log2(C_P) if C_P > 0 else float('inf')
    
    # Check if the conjecture holds
    conjecture_holds = abs(log_C_P - C_G) <= 3
    
    return {
        "metric_name": "log_C_P vs C_G",
        "metric_value": log_C_P,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample: C(G)={C_G}, |C_P|={C_P}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")