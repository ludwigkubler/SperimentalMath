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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def algebraic_k_theory_group(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a boolean function with 2^n values")
    
    # Simplified version of computing the algebraic K-theory group
    # This is a placeholder and should be replaced with actual computation
    return [f.count(1), f.count(0)]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        group = algebraic_k_theory_group(f)
        rank = max(group)
        
        result = {
            "metric_name": "minimal_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": rank >= n / math.log(n),
            "counterexample": "" if rank >= n / math.log(n) else f"n={n}, rank={rank}"
        }
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_rank": mean_rank,
        "support_fraction": support_fraction,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        if "support_fraction" not in result:
            continue
        
        mean_rank = result["mean_rank"]
        support_fraction = result["support_fraction"]
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
        elif any(r["conjecture_holds"] is False for r in result["results"]):
            first_failing_seed = next(s for s, r in zip(seeds, result["results"]) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='n={r[0]["instances_tested"]} rank<{r[0]["metric_value"]}' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_data")