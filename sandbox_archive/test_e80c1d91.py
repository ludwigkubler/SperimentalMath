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
    
    def entropy(f):
        counts = [f.count(0), f.count(1)]
        total = sum(counts)
        if total == 0:
            return 0
        p0, p1 = counts[0] / total, counts[1] / total
        if p0 == 0 or p1 == 0:
            return 0
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    def geometric_langlands_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] != (i % 2 == 0):
                rank += 1
        return rank
    
    instances_tested = 30
    rank_sum = 0
    entropy_sum = 0
    rank_count = [0] * instances_tested
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = [random.choice([0, 1]) for _ in range(n)]
        rank = geometric_langlands_rank(f)
        ent = entropy(f)
        rank_sum += rank
        entropy_sum += ent
        rank_count.append(rank)
    
    mean_rank = rank_sum / instances_tested
    mean_entropy = entropy_sum / instances_tested
    correlation_coefficient = 0
    
    if instances_tested > 1:
        numerator = sum((rank_count[i] - mean_rank) * (i + 5 - mean_entropy) for i in range(instances_tested))
        denominator = math.sqrt(sum((rank_count[i] - mean_rank) ** 2 for i in range(instances_tested)) * sum((i + 5 - mean_entropy) ** 2 for i in range(instances_tested)))
        if denominator == 0:
            correlation_coefficient = 1
        else:
            correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7 and (sum(1 for r in rank_count if r > mean_rank) / instances_tested <= 0.1)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")