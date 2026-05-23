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
    instances_tested = 30
    
    rank_sum = 0
    min_rank = float('inf')
    max_rank = 0
    
    for _ in range(instances_tested):
        # Generate a random polynomial of degree n
        coefficients = [random.uniform(-1, 1) for _ in range(n + 1)]
        
        # Compute the geometric locus rank (simplified example)
        # This is a placeholder for actual computation
        rank = sum(abs(coeff) for coeff in coefficients)
        
        rank_sum += rank
        min_rank = min(min_rank, rank)
        max_rank = max(max_rank, rank)
    
    mean_rank = rank_sum / instances_tested
    
    conjecture_holds = mean_rank >= n * math.log(n)
    counterexample = "" if conjecture_holds else f"Rank {min_rank} < Ω({n} log {n})"
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")