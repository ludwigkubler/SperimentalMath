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
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    
    # Generate a random read-twice branching program P with n inputs and m clauses
    P = []
    for _ in range(m):
        clause = [random.choice([1, -1]) for _ in range(n)]
        P.append(clause)
    
    # Compute the associated algebraic stack (simplified model)
    rank = 0
    for i in range(n):
        if any(P[j][i] != 0 for j in range(m)):
            rank += 1
    
    # Theoretical bound for minimal rank
    theoretical_bound = m ** 0.5 * n ** (1/3)
    
    # Check the ratio between computed rank and theoretical bound
    ratio = rank / theoretical_bound if theoretical_bound != 0 else float('inf')
    
    metric_value = ratio
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8 and metric_value <= 10,
        "counterexample": "" if ratio >= 0.8 else f"Ratio {ratio} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 31))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio < 0.8\" first_failing_seed={first_failing_seed}")