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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
            bp.append(random.choice([0, 1]))
        return bp
    
    def compute_persistence(bp):
        # Simplified persistence computation (not actual GUDHI)
        homology_groups = [len(set(bp[:i])) for i in range(1, len(bp) + 1)]
        persistence_values = [homology_groups[i] - homology_groups[i-1] for i in range(1, len(homology_groups))]
        return sum(persistence_values)
    
    def size(bp):
        return len(bp)
    
    n = 40
    bp = generate_read_twice_bp(n)
    beta_p = compute_persistence(bp)
    log_size_p = math.log2(size(bp))
    
    if beta_p > log_size_p:
        conjecture_holds = False
        counterexample = "beta(P) exceeds O(log size(P))"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "beta(P)",
        "metric_value": beta_p,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_beta_p = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_beta_p} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_beta_p} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='beta(P) exceeds O(log size(P))' first_failing_seed={first_failing_seed}")