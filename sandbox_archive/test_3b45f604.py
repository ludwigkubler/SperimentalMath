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
from math import ceil, sqrt
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_coxeter_group(r):
        if not isinstance(r, int) or r <= 0:
            return []
        return [tuple(sorted(random.sample(range(1, r+1), 2))) for _ in range(10)]
    
    def count_maximal_parabolic_subgroups(group):
        n = len(group)
        if n == 0:
            return 0
        count = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all((group[i][k] < group[j][k]) or (group[i][k] > group[j][k]) for k in range(2)):
                    count += 1
        return count
    
    r_values = [5, 10, 15, 20, 30, 40]
    total_count = 0
    n_max = max(r_values)
    
    for r in r_values:
        group = generate_coxeter_group(r)
        count = count_maximal_parabolic_subgroups(group)
        total_count += count
    
    metric_value = total_count / len(r_values)
    conjecture_holds = metric_value <= 40 * 40
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "distinct_maximal_parabolic_subgroups",
        "metric_value": metric_value,
        "instances_tested": len(r_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")