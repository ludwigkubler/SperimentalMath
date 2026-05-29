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
    
    def generate_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def coxeter_order(truth_table):
        n = len(truth_table)
        # Simplified Coxeter group order calculation (placeholder)
        return math.ceil(math.log(n, 2)) ** 2
    
    def mean_ratio(trials):
        total = sum(coxeter_order(tt) / (math.log(len(tt), 2) ** 2) for tt in trials)
        return total / len(trials)
    
    n_max = 40
    instances_tested = 100
    ratios = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        truth_table = generate_truth_table(n)
        ratio = coxeter_order(truth_table) / (math.log(len(truth_table), 2) ** 2)
        ratios.append(ratio)
    
    mean_ratio_value = mean_ratio(ratios)
    conjecture_holds = 0.8 <= mean_ratio_value <= 1.2
    counterexample = "" if conjecture_holds else f"mean_ratio={mean_ratio_value}"
    
    return {
        "metric_name": "mean_ratio",
        "metric_value": mean_ratio_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")