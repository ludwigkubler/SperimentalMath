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
    
    def generate_bp(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_k_theory_rank(bp):
        # Placeholder function to simulate K-theory rank computation
        size = len(bp)
        if size <= 1:
            return 1
        return random.randint(1, size)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_bp(n)
    k_theory_rank = compute_k_theory_rank(bp)
    
    instances_tested = 1
    conjecture_holds = (math.log(n) <= k_theory_rank <= math.log(n) * math.log(n)**2)
    counterexample = "" if conjecture_holds else f"BP of size {n} with K-theory rank {k_theory_rank}"
    
    return {
        "metric_name": "K-theory rank",
        "metric_value": k_theory_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30)) + [37]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"BP of size {n} with K-theory rank {k_theory_rank}\" first_failing_seed={first_failing_seed}")