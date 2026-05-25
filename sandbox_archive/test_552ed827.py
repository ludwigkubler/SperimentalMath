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
    
    def generate_graph(n, m):
        edges = set()
        while len(edges) < m:
            u, v = random.sample(range(n), 2)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)

    def is_coxeter_group(permutation):
        n = len(permutation)
        for i in range(n):
            for j in range(i + 1, n):
                if permutation[i] == permutation[j]:
                    continue
                k = (permutation.index(permutation[i], j) - j) % n
                if permutation[(i + k) % n] != permutation[j]:
                    return False
        return True

    def communication_complexity(graph, k):
        n = len(graph)
        edges = set(graph)
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in edges and (j, i) not in edges:
                    return float('inf')
        return min(k, n - k)

    def permutation_group(permutation):
        n = len(permutation)
        group = set()
        for i in range(n):
            permuted = [permutation[(i + j) % n] for j in range(n)]
            group.add(tuple(permuted))
        return group

    n = random.randint(5, 40)
    m = random.randint(int(0.1 * n * (n - 1)), int(0.9 * n * (n - 1)))
    graph = generate_graph(n, m)
    k = random.randint(3, min(n, 6))

    permutation = list(range(n))
    random.shuffle(permutation)
    group = permutation_group(permutation)

    if is_coxeter_group(group):
        cc = communication_complexity(graph, k)
        bound = k**(2/3) * n**(1/3)
        return {
            "metric_name": "communication_complexity",
            "metric_value": cc,
            "instances_tested": 1,
            "conjecture_holds": cc <= bound,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "communication_complexity",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")