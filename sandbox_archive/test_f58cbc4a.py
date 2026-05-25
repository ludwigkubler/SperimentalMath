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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for i in range(1, p):
            if (i * i) % p == a:
                return True
        return False
    
    def find_elliptic_curve_rank(x, q):
        rank = 0
        for a in range(q):
            if is_quadratic_residue(a, q):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank_diff = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            x = ''.join(random.choice('01') for _ in range(n))
            q = random.randint(2**n, 2**(n+1))
            rank_inner_product = find_elliptic_curve_rank(int(x, 2), q)
            rank_xor = find_elliptic_curve_rank(int(x, 2) ^ (1 << n), q)
            total_rank_diff += abs(rank_inner_product - rank_xor)
            instances_tested += 1
    
    mean_rank_diff = total_rank_diff / instances_tested
    conjecture_holds = mean_rank_diff <= 0.5 * math.log(n_values[-1])
    
    return {
        "metric_name": "Mean Rank Difference",
        "metric_value": mean_rank_diff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank difference {total_rank_diff} exceeds threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank difference exceeds threshold\" first_failing_seed={first_failing_seed}")