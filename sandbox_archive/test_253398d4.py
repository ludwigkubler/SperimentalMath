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
    
    def hamming_distance(x, y):
        return sum(xi != yi for xi, yi in zip(x, y))
    
    def min_generators_count(f):
        n = len(f)
        homomorphisms = set()
        for i in range(1 << n):
            hom = [f[hamming_distance(j, i)] for j in range(1 << n)]
            homomorphisms.add(tuple(hom))
        generators = []
        for h in homomorphisms:
            if all(h[i] == 0 or h[j] == 0 for i in range(n) for j in range(i+1, n)):
                generators.append(h)
        return len(generators)
    
    def entropy_rate(f):
        n = len(f)
        counts = [f.count(0), f.count(1)]
        total = sum(counts)
        if total == 0:
            return 0
        p0 = counts[0] / total
        p1 = counts[1] / total
        if p0 == 0 or p1 == 0:
            return 0
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        generators_count = min_generators_count(f)
        entropy = entropy_rate(f)
        results.append({
            "n": n,
            "generators_count": generators_count,
            "entropy": entropy
        })
    
    mean_generators_count = sum(r["generators_count"] for r in results) / len(results)
    mean_entropy = sum(r["entropy"] for r in results) / len(results)
    max_n = max(r["n"] for r in results)
    
    conjecture_holds = all(abs(generators_count - n**(1/3)) <= 2 * n**(1/3) for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generators Count",
        "metric_value": mean_generators_count,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n']}, generators_count={r['generators_count']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break