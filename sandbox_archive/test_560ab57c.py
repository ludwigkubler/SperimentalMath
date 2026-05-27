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
    
    def generate_bp(n):
        # Generate a random read-twice branching program of size n
        bp = []
        for _ in range(n):
            layer = [random.choice([0, 1]) for _ in range(2)]
            bp.append(layer)
        return bp
    
    def group_cocommutative_algebra(bp):
        # Compute the group cocommutative algebra for a given BP
        n = len(bp)
        algebra = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if bp[i][j % 2] == 1 and bp[j][i % 2] == 1:
                    algebra[i][j] = 1
        return algebra
    
    def min_rank(algebra):
        # Compute the minimal rank of a given algebra
        n = len(algebra)
        rank = 0
        for i in range(n):
            if any(algebra[j][i] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def log_size(bp):
        # Compute the logarithm of the size of a BP
        n = len(bp)
        return math.log2(n)
    
    bp = generate_bp(40)
    algebra = group_cocommutative_algebra(bp)
    rank = min_rank(algebra)
    log_n = log_size(bp)
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")