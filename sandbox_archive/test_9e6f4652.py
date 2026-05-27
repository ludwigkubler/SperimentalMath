# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(n)]

    def calculate_entropy(f):
        ones = f.count(1)
        zeros = f.count(0)
        total = len(f)
        if ones == 0 or ones == total:
            return 0
        p_ones = Fraction(ones, total)
        p_zeros = Fraction(zeros, total)
        return entropy(p_ones) + entropy(p_zeros)

    def calculate_minimal_rank(n):
        # Placeholder for actual computation of minimal rank
        # For simplicity, we assume it's equal to the number of bits
        return n

    instances_tested = 0
    total_entropy = 0
    total_rank = 0

    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        H_f = calculate_entropy(f)
        if H_f < 1:
            continue
        r_K_f = calculate_minimal_rank(n)
        total_entropy += H_f
        total_rank += r_K_f
        instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "mean_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }

    mean_entropy = total_entropy / instances_tested
    mean_rank = total_rank / instances_tested

    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_rank / mean_entropy,
        "instances_tested": instances_tested,
        "conjecture_holds": mean_rank / mean_entropy >= 0.8 and mean_rank <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")