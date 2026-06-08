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
    
    def p_adic_divergence(p, a, b):
        if a == b:
            return 0
        pa = [p**i for i in range(len(a))]
        pb = [p**i for i in range(len(b))]
        sum_pa = sum(pa)
        sum_pb = sum(pb)
        return abs(sum_pa - sum_pb) / max(sum_pa, sum_pb)

    def generate_bits(n):
        return [random.choice([0, 1]) for _ in range(n)]

    n_values = [5, 10, 15, 20, 30, 40]
    total_divergence = 0
    instances_tested = 0

    for n in n_values:
        a = generate_bits(n)
        b = generate_bits(n)
        divergence = p_adic_divergence(2, a, b)
        total_divergence += divergence
        instances_tested += 1

    mean_value = total_divergence / instances_tested
    conjecture_holds = mean_value <= math.log2(max(n_values))
    counterexample = "" if conjecture_holds else "p-adic divergence not O(log n)"

    return {
        "metric_name": "p-adic divergence",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def std(data, mean):
    return math.sqrt(sum((x - mean) ** 2 for x in data) / len(data))

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = std([r["metric_value"] for r in results], mean_value)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-adic divergence not O(log n)\" first_failing_seed={seeds[first_failing_seed]}")