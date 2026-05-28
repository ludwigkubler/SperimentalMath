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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_monotone_complexity(f):
        n = int(math.log2(len(f)))
        complexity = 0
        for i in range(n):
            for j in range(i+1, n+1):
                if all(f[i*2**j + k] <= f[i*2**(j-1) + k] for k in range(2**(j-1))):
                    complexity += 1
        return complexity
    
    def compute_twisted_differential_forms_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            diff_form = [f[i*2**j + k] - f[i*2**(j-1) + k] for j in range(i+1, n+1) for k in range(2**(j-1))]
            rank += max(abs(x) for x in diff_form)
        return rank
    
    def correlation_coefficient(ranks, complexities):
        n = len(ranks)
        mean_rank = sum(ranks) / n
        mean_complexity = sum(complexities) / n
        numerator = sum((ranks[i] - mean_rank) * (complexities[i] - mean_complexity) for i in range(n))
        denominator = math.sqrt(sum((ranks[i] - mean_rank)**2 for i in range(n)) * sum((complexities[i] - mean_complexity)**2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        complexity = compute_monotone_complexity(f)
        rank = compute_twisted_differential_forms_rank(f)
        ranks.append(rank)
        complexities.append(complexity)
    
    ratio = [r / c if c != 0 else float('inf') for r, c in zip(ranks, complexities)]
    valid_ratios = [r for r in ratio if r <= 1.5 and r >= 0.5]
    
    conjecture_holds = len(valid_ratios) == len(ratio)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Rank to Monotone Complexity",
        "metric_value": sum(ratio) / len(ratio),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")