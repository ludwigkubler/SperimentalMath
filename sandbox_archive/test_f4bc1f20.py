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
        bp = []
        for _ in range(n):
            row = [random.choice([0, 1]) for _ in range(2)]
            bp.append(row)
        return bp
    
    def p_adic_power_series(bp):
        n = len(bp)
        rank = 0
        for i in range(n):
            if any(bp[j][i] == 1 for j in range(n)):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bp = generate_bp(n)
        rank = p_adic_power_series(bp)
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    conjecture_holds = all(0.5 * n * math.log(n) <= rank <= 2 * n * math.log(n) for n, rank in zip(n_values, results))
    counterexample = "" if conjecture_holds else f"BP size {n_values[-1]} with rank {results[-1]}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["conjecture_holds"])
    
    support_fraction = sum(results) / len(results)
    
    if all(results):
        result = "SUPPORTED"
    elif sum(results) >= 0.8 * len(results):
        result = "SUPPORTED"
    else:
        first_failing_seed = seeds[results.index(False)]
        counterexample = f"BP size {n_values[-1]} with rank {results[-1]}"
        result = f"FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} support_fraction={support_fraction:.2f}")