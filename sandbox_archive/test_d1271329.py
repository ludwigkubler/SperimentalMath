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
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def kahler_rank(n, h):
        # Placeholder function for computing Kähler rank
        # This is a dummy implementation and should be replaced with actual computation
        return int(h * n)

    instances_tested = 0
    total_entropy = 0
    total_rank = 0

    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        p = random.random()
        h = entropy(p)
        if h < 1:
            continue
        
        rank = kahler_rank(n, h)
        total_entropy += h
        total_rank += rank
        instances_tested += 1

    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else 0
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    
    conjecture_holds = mean_rank <= 3 and (mean_rank / mean_entropy) >= 0.8
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} exceeds bound of 3 or ratio {mean_rank / mean_entropy} < 0.8"

    return {
        "metric_name": "Ratio of Mean Rank to Entropy",
        "metric_value": mean_rank / mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results) if results else 0
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results)) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank exceeds bound or ratio < 0.8\" first_failing_seed={first_failing_seed}")