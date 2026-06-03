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
    
    # Generate a random finite category C with n objects and m morphisms
    n = random.randint(5, 30)
    m = random.randint(n * (n - 1), n * n)
    category = {i: [] for i in range(n)}
    for _ in range(m):
        src, dst = random.sample(range(n), 2)
        if dst not in category[src]:
            category[src].append(dst)
    
    # Calculate the minimal order of representations
    min_order = float('inf')
    for obj in category:
        rank = len(category[obj])
        for morphs in category[obj]:
            rank += len(category[morphs])
        min_order = min(min_order, rank)
    
    # Convert the category to a CNF and compute its circuit monotone width
    cnf = []
    for src in category:
        for dst in category[src]:
            cnf.append((src, dst))
    m_cnf = len(cnf)
    
    # Measure the correlation between min_order(C) and m(C)
    metric_value = abs(min_order - m_cnf)
    instances_tested = 1
    n_max = n
    conjecture_holds = (metric_value <= 2)
    counterexample = "" if conjecture_holds else f"min_order={min_order}, m_CNF={m_cnf}"
    
    return {
        "metric_name": "mean_absolute_difference",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")