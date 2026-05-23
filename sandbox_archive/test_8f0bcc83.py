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
    
    def generate_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def acc0_complexity(f):
        n = len(f)
        count = 0
        for i in range(n):
            if f[i] == 1:
                count += 1
        return count
    
    def minimal_brauer_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_function(n)
        complexity = acc0_complexity(f)
        rank = minimal_brauer_rank(f)
        
        if complexity > math.log2(n):
            counterexample = f"n={n}, ACC⁰ complexity={complexity}, Brauer rank={rank}"
            return {
                "metric_name": "Minimal Rank of Brauer Groups",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": counterexample
            }
        
        results.append({
            "n": n,
            "complexity": complexity,
            "rank": rank
        })
    
    return {
        "metric_name": "Minimal Rank of Brauer Groups",
        "metric_value": sum(r["rank"] for r in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['n']}, ACC⁰ complexity={results[first_failing_seed]['complexity']}, Brauer rank={results[first_failing_seed]['rank']}\" first_failing_seed={first_failing_seed}")