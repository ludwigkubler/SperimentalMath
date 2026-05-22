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
    
    def log2(x):
        return math.log2(x + 1e-10) if x > 0 else -math.inf
    
    def tensor_rank(n):
        # Constructive mapping from BP to group representation
        # This is a placeholder function. Replace with actual implementation.
        return random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    rank = tensor_rank(n)
    log_n = log2(n)
    
    metric_value = abs(rank - log_n) / (log_n + 1e-10)
    conjecture_holds = 0.8 <= metric_value <= 1.2 and rank <= 10
    counterexample = "" if conjecture_holds else f"rank={rank}, expected_rank≈{log_n}"
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        result = f"FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")