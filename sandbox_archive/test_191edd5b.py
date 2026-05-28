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
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    def min_rank(n):
        # Placeholder for actual computation of minimal rank
        # This is a dummy implementation that does not actually compute the rank
        return random.randint(1, n)
    
    def f(n):
        return n
    
    c_f = 1.2  # Example constant, adjust as needed
    
    results = []
    for n in range(5, 41):
        rank = min_rank(n)
        expected = c_f * log2(f(n))
        results.append({
            "n": n,
            "rank": rank,
            "expected": expected
        })
    
    metric_value = sum(r["rank"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["rank"] >= r["expected"] for r in results)
    counterexample = "" if conjecture_holds else f"Rank {results[0]['rank']} is less than expected {results[0]['expected']}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")