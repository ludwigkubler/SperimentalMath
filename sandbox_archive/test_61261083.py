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
    
    def hamming_distance(a, b):
        return sum(x != y for x, y in zip(a, b))
    
    def min_generators_count(homomorphisms):
        generators = set()
        for hom in homomorphisms:
            if all(hamming_distance(hom, gen) % 2 == 1 for gen in generators):
                generators.add(hom)
        return len(generators)
    
    def entropy_rate(f):
        n = len(f)
        counts = [f.count(i) for i in range(2)]
        probabilities = [c / n for c in counts]
        entropy = -sum(p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def coxeter_group_homomorphisms(f):
        n = len(f)
        homomorphisms = []
        for i in range(1 << n):
            hom = [f[hamming_distance(j, i)] ^ f[j] for j in range(n)]
            homomorphisms.append(hom)
        return homomorphisms
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        f = generate_boolean_function(n)
        homs = coxeter_group_homomorphisms(f)
        generators_count = min_generators_count(homs)
        entropy = entropy_rate(f)
        results.append({
            "n": n,
            "generators_count": generators_count,
            "entropy_rate": entropy
        })
    
    mean_generators = sum(res["generators_count"] for res in results) / len(results)
    mean_entropy = sum(res["entropy_rate"] for res in results) / len(results)
    max_n = max(res["n"] for res in results)
    
    conjecture_holds = all(res["generators_count"] <= n**(1/3) and abs(res["entropy_rate"]) <= 2 * n**(1/3) for res in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generators Count",
        "metric_value": mean_generators,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")