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
    return [random.randint(0, 1) for _ in range(2**n)]

def resolution_width(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a Boolean function with 2^n values")
    
    def solve(lits_true, lits_false, cls=None):
        if not lits_true and not lits_false:
            return False
        if not lits_true:
            return True
        
        lit = lits_true[0]
        other_lit = -lit
        
        new_lits_true = [l for l in lits_true if l != other_lit]
        new_lits_false = [l for l in lits_false if l != other_lit]
        
        return solve(new_lits_true, cls) or solve(new_lits_false, cls)
    
    return 1 + max(solve([i], []) for i in range(2**n))

def noncrossing_partition(f):
    n = int(math.log2(len(f)))
    if len(f) != 2**n:
        raise ValueError("Input must be a Boolean function with 2^n values")
    
    def partition(lits, depth=0):
        if not lits:
            return []
        
        lit = lits[0]
        other_lit = -lit
        
        true_lits = [l for l in lits if f[l] == 1]
        false_lits = [l for l in lits if f[l] == 0]
        
        return [(true_lits, false_lits)] + partition(true_lits, depth+1) + partition(false_lits, depth+1)
    
    return partition(list(range(2**n)))

def min_rank(partition):
    rank = 0
    for true_lits, false_lits in partition:
        rank += max(len(true_lits), len(false_lits))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    widths = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        partition = noncrossing_partition(f)
        rank = min_rank(partition)
        width = resolution_width(f)
        
        min_ranks.append(rank)
        widths.append(width)
    
    mean_rank = sum(min_ranks) / len(min_ranks)
    mean_width = sum(widths) / len(widths)
    ratio_mean = mean_rank / mean_width
    
    if 1.4 <= ratio_mean <= 1.6:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Ratio out of bounds: {ratio_mean}"
    
    return {
        "metric_name": "Minimal Rank / Resolution Width Ratio",
        "metric_value": ratio_mean,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")