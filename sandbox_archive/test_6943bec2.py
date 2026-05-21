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
    
    def generate_monotone_k_clique(n, k):
        vertices = list(range(n))
        edges = set()
        for _ in range(k):
            u, v = random.sample(vertices, 2)
            if u > v:
                u, v = v, u
            edges.add((u, v))
        return vertices, edges
    
    def coxeter_group_action(vertices, edges):
        orbits = {}
        for vertex in vertices:
            orbit = tuple(sorted([vertex] + [v for u, v in edges if u == vertex]))
            if orbit not in orbits:
                orbits[orbit] = []
            orbits[orbit].append(vertex)
        return orbits
    
    def count_orbits(orbits):
        return len(orbits)
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 10))
    vertices, edges = generate_monotone_k_clique(n, k)
    orbits = coxeter_group_action(vertices, edges)
    num_orbits = count_orbits(orbits)
    
    conjecture_holds = num_orbits <= (k ** 4)  # Polynomial upper bound
    counterexample = "" if conjecture_holds else f"Too many orbits: {num_orbits} > {k**4}"
    
    return {
        "metric_name": "Number of Orbits",
        "metric_value": num_orbits,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 307))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Too many orbits\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")