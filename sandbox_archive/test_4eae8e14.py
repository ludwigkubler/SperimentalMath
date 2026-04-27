# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random

def Q_dt(f):
    n = 16
    cache = {}
    
    def helper(x):
        if x not in cache:
            if len(x) == 1:
                return 0
            else:
                left = helper([f(xi, 0) for xi in range(n)])
                right = helper([f(xi, 1) for xi in range(n)])
                cache[x] = 1 + max(left, right)
        return cache[x]
    
    return helper(tuple(range(n)))

def RSK_insertion_tableau(arr):
    shape = [0]
    stack = []
    for x in arr:
        i = bisect_right(stack, x)
        if i == len(stack):
            stack.append(x)
            shape[-1] += 1
        else:
            stack[i] = x
    return shape

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k = 4
    n = 2**k
    
    def f(x, y):
        return (x >> (k - y)) & 1
    
    metric_name = "slack"
    instances_tested = 0
    total_slack = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for i in range(n):
        f_i = [f(i, j) for j in range(k)]
        pi_f = sorted(range(n), key=lambda x: (f(x, j) for j in range(k)))
        lambda_2_f = RSK_insertion_tableau(pi_f)[-1]
        
        slack = max(0, Q_dt(f_i) - math.ceil(math.log2(lambda_2_f + 1)))
        total_slack += slack
        instances_tested += 1
        
        if slack > 0:
            conjecture_holds = False
            counterexample = f"Function {i} has a slack of {slack}"
    
    mean_slack = total_slack / instances_tested
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_slack,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")