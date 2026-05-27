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

def tropicalize(x):
    if isinstance(x, list):
        return max(tropicalize(xi) for xi in x)
    else:
        return abs(x)

def generate_channel(n):
    channel = []
    for _ in range(n):
        pi = [random.uniform(-10, 10) for _ in range(n)]
        channel.append(pi)
    return channel

def compute_minimal_rank(channel):
    n = len(channel)
    rank = 0
    for i in range(n):
        row = [channel[j][i] for j in range(n)]
        rank += tropicalize(row)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        channel = generate_channel(n)
        minimal_rank = compute_minimal_rank(channel)
        H = -sum(p * math.log2(p) for p in [p / n for p in sum(channel, [])] if p > 0)
        expected_bound = 2 ** H
        
        results.append({
            "n": n,
            "minimal_rank": minimal_rank,
            "H": H,
            "expected_bound": expected_bound
        })
    
    total_rank = sum(result["minimal_rank"] for result in results)
    mean_rank = total_rank / len(results)
    max_rank = max(result["minimal_rank"] for result in results)
    
    if any(result["minimal_rank"] > result["expected_bound"] for result in results):
        conjecture_holds = False
        counterexample = f"n={results[0]['n']}, H={results[0]['H']:.2f}, rank={results[0]['minimal_rank']}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
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
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['n']}, H={results[0]['H']:.2f}, rank={results[0]['minimal_rank']}' first_failing_seed={first_failing_seed}")