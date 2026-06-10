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
    
    def generate_protocol(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def calculate_rank_variance(protocol):
        n = len(protocol)
        mean = sum(protocol) / n
        variance = sum((x - mean) ** 2 for x in protocol) / n
        return variance
    
    def construct_braided_algebra(protocol):
        n = len(protocol)
        braided_algebra = []
        for i in range(n):
            row = [0] * n
            for j in range(n):
                row[j] = protocol[i] * protocol[j]
            braided_algebra.append(row)
        return braided_algebra
    
    def calculate_min_rank(braided_algebra):
        n = len(braided_algebra)
        min_rank = float('inf')
        for i in range(1 << n):
            rank = 0
            for j in range(n):
                if (i >> j) & 1:
                    rank += sum(braided_algebra[j][k] for k in range(n))
            min_rank = min(min_rank, rank)
        return min_rank
    
    def correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    def p_value(r, n):
        t_statistic = r * math.sqrt((n - 2) / (1 - r**2))
        df = n - 2
        # Using the t-distribution table or a library function to find the p-value
        return 2 * (1 - Fraction(t_statistic).limit_denominator(1000000))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        protocol = generate_protocol(n)
        rank_variance = calculate_rank_variance(protocol)
        braided_algebra = construct_braided_algebra(protocol)
        min_rank = calculate_min_rank(braided_algebra)
        results.append((min_rank, rank_variance))
    
    x = [result[0] for result in results]
    y = [result[1] for result in results]
    r = correlation(x, y)
    p = p_value(r, len(results))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max([len(result[0]) for result in results]),
        "conjecture_holds": r >= 0.7 and p <= 0.05,
        "counterexample": "" if r >= 0.7 and p <= 0.05 else f"r={r}, p={p}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    std_r = math.sqrt(sum((r["metric_value"] - mean_r) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_r} std={std_r} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")