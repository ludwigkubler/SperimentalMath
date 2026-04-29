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

def generate_random_string(length):
    return ''.join(random.choice('01') for _ in range(length))

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def generate_instances(gadget, n):
    instances = []
    for i in range(n):
        x = generate_random_string(len(list(gadget.keys())[0][0]))
        y = generate_random_string(len(list(gadget.keys())[0][1]))
        instances.append((x, y))
    return instances

def euclidean_distance(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def generate_metric_gadget(k):
    gadget = {}
    for i in range(2**k):
        x = format(i, f'0{k}b')
        for j in range(2**k):
            y = format(j, f'0{k}b')
            d = hamming_distance(x, y)
            gadget[(x, y)] = d
    return gadget

def generate_protocol_pullback(gadget, protocol, n):
    pullback = {}
    for i in range(n):
        x, y = protocol[i]
        pullback[(i, x, y)] = gadget[(x, y)]
    return pullback

def compute_cover_multiplicity(pullback, n):
    cover = set()
    for i in range(n):
        for j in range(i+1, n):
            if pullback[(i, '0', '0')] + pullback[(j, '0', '0')] <= pullback[(i, '0', '0')]:
                cover.add((i, j))
    return len(cover)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    k = 5
    n = 6
    f = "Disjointness"  # or "Inner Product"
    Q_f = n
    
    gadget = generate_metric_gadget(k)
    protocol = [(generate_random_string(k), generate_random_string(k)) for _ in range(n)]
    pullback = generate_protocol_pullback(gadget, protocol, n)
    
    cover_multiplicity = compute_cover_multiplicity(pullback, n)
    R_pi = max(pullback.values())
    alpha = math.log2(2)
    m_pi_bound = 2 ** (Q_f - alpha * Q_f)
    
    conjecture_holds = cover_multiplicity > m_pi_bound
    counterexample = "" if conjecture_holds else "multiplicity_not_sparse"
    
    return {
        "metric_name": "cover_multiplicity",
        "metric_value": cover_multiplicity,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"multiplicity_not_sparse\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")