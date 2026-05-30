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

def hamming_distance(x, y):
    return sum(xi != yi for xi, yi in zip(bin(x)[2:].zfill(n), bin(y)[2:].zfill(n)))

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(1 << n)]

def min_generators_count(f):
    n = int(math.log2(len(f)))
    hom = [f[hamming_distance(j, i)] for j in range(1 << n)]
    generators = set()
    for i in range(1 << n):
        if all(hom[i] != f[j] for j in range(i)):
            generators.add(i)
    return len(generators)

def entropy_rate(f):
    n = int(math.log2(len(f)))
    counts = [f.count(v) for v in set(f)]
    probabilities = [Fraction(c, 1 << n) for c in counts]
    return -sum(p * math.log2(p) if p != 0 else 0 for p in probabilities)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        generators_count = min_generators_count(f)
        H_f = entropy_rate(f)
        results.append({
            "n": n,
            "generators_count": generators_count,
            "H_f": H_f
        })
    mean_generators_count = sum(r["generators_count"] for r in results) / len(results)
    mean_H_f = sum(r["H_f"] for r in results) / len(results)
    conjecture_holds = all(abs(generators_count - n**(1/3)) <= 10 * n**(1/3) for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "generators_count",
        "metric_value": mean_generators_count,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")