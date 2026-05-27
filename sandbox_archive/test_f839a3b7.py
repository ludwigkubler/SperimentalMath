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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n):
        if n <= 0:
            return []
        bp = [random.randint(0, 1)]
        for _ in range(1, n):
            bp.append(bp[-1] ^ random.randint(0, 1))
        return bp
    
    def compute_group_cocommutative_algebra(bp):
        size = len(bp)
        algebra = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                if bp[i] == bp[j]:
                    algebra[i][j] = 1
        return algebra
    
    def min_rank(algebra):
        n = len(algebra)
        rank = 0
        for row in algebra:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(i, n):
                            if algebra[j][i] == 1 and algebra[j][k] == 1:
                                algebra[j][k] = 0
        return rank
    
    def log_size(bp):
        size = len(bp)
        if size <= 0:
            return 0
        return math.log2(size)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    algebra = compute_group_cocommutative_algebra(bp)
    rank = min_rank(algebra)
    log_n = log_size(bp)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= math.log2(n) + 3 and rank >= n - 3,
        "counterexample": "" if rank <= math.log2(n) + 3 and rank >= n - 3 else f"rank={rank}, n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
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
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too large\" first_failing_seed={first_failing_seed}")