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
    p = 2  # Fixed prime for p-adic expansion
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_rank = 0.0
    total_variance = 0.0
    rank_values = []
    variance_values = []

    random.seed(seed)

    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            protocol = [random.randint(0, 1) for _ in range(n)]
            bits_communicated = sum(protocol)
            rank_value = len(set(p_adic_expansion(p, bits_communicated)))
            variance_value = bits_communicated / n

            total_rank += rank_value
            total_variance += variance_value
            instances_tested += 1
            rank_values.append(rank_value)
            variance_values.append(variance_value)

    rank_mean = total_rank / instances_tested
    variance_mean = total_variance / instances_tested

    if instances_tested == 0:
        correlation = None
    else:
        numerator = sum((rank_value - rank_mean) * (variance_value - variance_mean) for rank_value, variance_value in zip(rank_values, variance_values))
        denominator = math.sqrt(instances_tested * sum((rank_value - rank_mean) ** 2 for rank_value in rank_values)) * math.sqrt(instances_tested * sum((variance_value - variance_mean) ** 2 for variance_value in variance_values))
        correlation = numerator / denominator if denominator != 0 else None

    conjecture_holds = correlation is not None and correlation >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation: {correlation}"

    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def p_adic_expansion(p: int, n: int) -> list:
    if n == 0:
        return [0]
    expansion = []
    while n > 0:
        remainder = n % p
        expansion.append(remainder)
        n //= p
    return expansion

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")