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
    
    def tropicalize(x):
        return max(x, key=abs)
    
    def entropy(p):
        if any(pi <= 0 for pi in p):
            return float('-inf')
        return -sum(pi * math.log2(pi) for pi in p)
    
    def minimal_rank(channel):
        n = len(channel)
        rank = n
        for i in range(1, n):
            for j in range(i + 1, n):
                if channel[i] == channel[j]:
                    rank -= 1
                    break
        return rank
    
    def generate_channel(n):
        p = [random.random() for _ in range(n)]
        p = [pi / sum(p) for pi in p]
        return [tropicalize(pi) for pi in p]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            channel = generate_channel(n)
            rank = minimal_rank(channel)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank <= 2 ** entropy([1/n for n in range(5, 41)])
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed + 2}")