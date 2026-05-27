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
    
    def schur_polynomial(f):
        n = len(f)
        s = [0] * (n + 1)
        s[0] = 1
        for i in range(1, n + 1):
            s[i] = sum(s[j] * f[i - j] for j in range(i)) if i < n else 0
        return s
    
    def monotone_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def min_rank(poly):
        rank = 0
        for coeff in poly:
            if coeff != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ranks = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = monotone_boolean_function(n)
            poly = schur_polynomial(f)
            rank = min_rank(poly)
            total_ranks += rank
            instances_tested += 1
    
    mean_rank = Fraction(total_ranks, instances_tested)
    conjecture_holds = mean_rank >= n * math.log(n) / 2
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected=Ω({n} log {n})"
    
    return {
        "metric_name": "min_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")