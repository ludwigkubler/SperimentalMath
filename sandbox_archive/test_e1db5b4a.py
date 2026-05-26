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
    
    def free_entropy(probabilities):
        return -sum(p * math.log2(p) for p in probabilities if p > 0)
    
    def generate_bp(n):
        size = 2 ** n
        bp = [random.random() for _ in range(size)]
        return bp
    
    def log_2_size(bp):
        return math.log2(len(bp))
    
    O_n = lambda n: random.uniform(0, 1) * n
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        bp = generate_bp(n)
        F_P = free_entropy(bp)
        upper_bound = log_2_size(bp) + O_n(n)
        metric_values.append((F_P, upper_bound))
    
    mean_value = sum(F_P - upper_bound for F_P, upper_bound in metric_values) / len(metric_values)
    max_diff = max(abs(F_P - upper_bound) for F_P, upper_bound in metric_values)
    
    conjecture_holds = all(abs(mean_value) <= 3 and max_diff <= 10 for _ in range(9))
    counterexample = "" if conjecture_holds else "mean_diff={}, max_diff={}".format(mean_value, max_diff)
    
    return {
        "metric_name": "free_entropy_bound",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.9:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))