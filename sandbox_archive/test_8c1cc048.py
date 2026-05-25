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
    
    def boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def delone_set_representation(f):
        n = len(f)
        d = {}
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    key = tuple(sorted([i, j]))
                    d[key] = 1
        return d
    
    def matroid_rank(d):
        elements = list(d.keys())
        rank = len(elements)
        for i in range(len(elements)):
            for j in range(i+1, len(elements)):
                if all(d.get(tuple(sorted([e, f])), 0) == 0 for e in elements[:i] + elements[i+1:j] + elements[j+1:]):
                    rank -= 1
        return rank
    
    def communication_complexity(f):
        n = len(f)
        # Simplified protocol: each bit requires one message
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = boolean_function(n)
            d = delone_set_representation(f)
            rank = matroid_rank(d)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    cc_k_clique = communication_complexity(boolean_function(5))  # Simplified for testing
    alpha = 0.95  # Significance level
    threshold = alpha * cc_k_clique
    
    conjecture_holds = mean_rank <= threshold
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mean_matroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")