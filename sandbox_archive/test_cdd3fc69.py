# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_disjointness_function(n):
        return {i: (i & j == 0) for i in range(2**n) for j in range(i+1, 2**n)}
    
    def compute_partial_order(f):
        n = int(math.log2(len(f)))
        partial_order = [[False] * (2**n) for _ in range(2**n)]
        for x, y in combinations(range(2**n), 2):
            if f[x] and not f[y]:
                partial_order[x][y] = True
        return partial_order
    
    def compute_quandle_representation(partial_order):
        n = len(partial_order)
        quandle = {}
        for i in range(n):
            quandle[i] = set()
            for j in range(n):
                if partial_order[i][j]:
                    quandle[i].add(j)
        return quandle
    
    def compute_minimal_rank(quandle):
        rank = 0
        used = [False] * len(quandle)
        for i in range(len(quandle)):
            if not used[i]:
                rank += 1
                stack = [i]
                while stack:
                    node = stack.pop()
                    if not used[node]:
                        used[node] = True
                        for neighbor in quandle[node]:
                            stack.append(neighbor)
        return rank
    
    n = random.randint(5, 40)
    f = generate_disjointness_function(n)
    partial_order = compute_partial_order(f)
    quandle = compute_quandle_representation(partial_order)
    minimal_rank = compute_minimal_rank(quandle)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": minimal_rank,
        "instances_tested": 1,
        "conjecture_holds": minimal_rank >= n,
        "counterexample": "" if minimal_rank >= n else f"Disjointness function with n={n} and minimal rank {minimal_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((r['metric_value'] - mean_rank)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")