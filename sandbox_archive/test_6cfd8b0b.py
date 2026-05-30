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

def hamming_distance(a, b):
    return sum(x != y for x, y in zip(bin(a)[2:].zfill(30), bin(b)[2:].zfill(30)))

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def coxeter_group_homomorphisms(f):
    n = int(math.log2(len(f)))
    homs = []
    for i in range(2**n):
        hom = [f[hamming_distance(j, i)] ^ f[j] for j in range(2**n)]
        if len(set(hom)) == 2:
            homs.append(hom)
    return homs

def minimal_generators(homs):
    n = int(math.log2(len(homs[0])))
    generators = set()
    for hom in homs:
        for i in range(n):
            if all(hom[j] ^ hom[j ^ (1 << i)] == hom[j] for j in range(2**n)):
                generators.add(i)
    return len(generators)

def entropy_rate(f):
    n = int(math.log2(len(f)))
    counts = [f.count(i) for i in range(2)]
    total = sum(counts)
    if total == 0:
        return 0
    p0 = Fraction(counts[0], total)
    p1 = Fraction(counts[1], total)
    if p0 == 0 or p1 == 0:
        return 0
    return -p0 * math.log2(p0) - p1 * math.log2(p1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    homs = coxeter_group_homomorphisms(f)
    num_generators = minimal_generators(homs)
    H_f = entropy_rate(f)
    k = 2.0  # Example constant
    conjecture_holds = abs(H_f) <= k * n**(1/3)
    counterexample = "" if conjecture_holds else f"Entropy rate {H_f} not within factor {k} of {n**(1/3)}"
    return {
        "metric_name": "Number of Minimal Generators",
        "metric_value": num_generators,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")