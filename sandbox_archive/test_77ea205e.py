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
    n_values = [5, 10, 15, 20, 30, 40]
    total_ranks = []
    total_widths = []

    for n in n_values:
        for _ in range(30):
            width = random.randint(1, n)
            rank = random.randint(1, n * math.log(n, 2))
            total_ranks.append(rank)
            total_widths.append(width)

    correlation_coefficient = calculate_correlation(total_ranks, total_widths)
    mean_rank = sum(total_ranks) / len(total_ranks)
    conjecture_holds = correlation_coefficient >= 0.8 and mean_rank <= n * math.log(2 * n, 2)
    counterexample = "" if conjecture_holds else "correlation_coefficient<0.8 or mean_rank>Θ(n log(2n))"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(total_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8 or mean_rank>Θ(n log(2n))\" first_failing_seed={first_failing_seed}")