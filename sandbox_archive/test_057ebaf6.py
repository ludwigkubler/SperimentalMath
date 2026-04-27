# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def memoize(f):
    cache = {}
    def helper(x):
        if x not in cache:            
            cache[x] = f(x)
        return cache[x]
    return helper

@memoize
def Q_dt(g, k=4):
    if len(g) == 1:
        return 0
    else:
        i = g.index(min(g))
        return 1 + max(Q_dt(g[:i], k), Q_dt(g[i+1:], k))

def RSK_insertion_tableau(seq):
    tableau = []
    for x in seq:
        row = []
        while row and row[-1] > x:
            row.pop()
        row.append(x)
        if len(row) > len(tableau):
            tableau.append([])
        tableau[len(row)-1].append(x)
    return tableau

def lambda_2(f, k=4):
    seq = sorted(range(2**k), key=lambda x: (f(x), x))
    tableau = RSK_insertion_tableau(seq)
    return len(tableau)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 14
    k = 4
    
    results = []
    for _ in range(2**k):
        f = [random.randint(0, 1) for _ in range(2**k)]
        
        q_dt_f = Q_dt(f)
        lambda_2_f = lambda_2(f)
        
        slack = math.ceil(math.log2(lambda_2_f + 1)) - q_dt_f
        results.append((q_dt_f, lambda_2_f, slack))
    
    total_slack = sum(slack for _, _, slack in results)
    avg_slack = total_slack / len(results)
    std_dev = math.sqrt(sum((slack - avg_slack) ** 2 for _, _, slack in results) / len(results))
    
    conjecture_holds = all(q_dt_f >= math.ceil(math.log2(lambda_2_f + 1)) for q_dt_f, lambda_2_f, _ in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "slack",
        "metric_value": avg_slack,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
    
    results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            trial_result = json.load(f)["TRIAL"]
            results.append(trial_result["metric_value"])
    
    avg_metric_value = sum(results) / len(results)
    std_dev_metric_value = math.sqrt(sum((x - avg_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= avg_metric_value) / len(results)
    
    if all(r >= avg_metric_value for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(r < avg_metric_value for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result < avg_metric_value)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")