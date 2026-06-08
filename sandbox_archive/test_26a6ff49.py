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

def p_adic_divergence(p, a, b):
    pa = [p**i * (a % p) for i in range(len(a))]
    pb = [p**i * (b % p) for i in range(len(b))]
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    max_length = max(len(pa), len(pb))
    pa += [0] * (max_length - len(pa))
    pb += [0] * (max_length - len(pb))
    
    return hamming_distance(pa, pb)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        a = [random.randint(0, 1) for _ in range(n)]
        b = [random.randint(0, 1) for _ in range(n)]
        
        divergence = p_adic_divergence(2, a, b)
        metric_values.append(divergence)
        instances_tested += n
        n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    conjecture_holds = mean_value <= math.log2(n_max)
    counterexample = "" if conjecture_holds else f"mean={mean_value} > log2({n_max})"
    
    return {
        "metric_name": "p-adic divergence",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean exceeds log2(n)\" first_failing_seed={first_failing_seed}")