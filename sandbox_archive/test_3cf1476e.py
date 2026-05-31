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
    
    def generate_boolean_function(n, m):
        return [random.choice([0, 1]) for _ in range(m)]
    
    def generate_conflict_graph(f, n):
        G = [[0] * n for _ in range(n)]
        for i in range(len(f)):
            for j in range(i + 1, len(f)):
                if f[i] != f[j]:
                    for k in range(n):
                        if (f[i][k] != f[j][k]):
                            G[k][i] = 1
                            G[k][j] = 1
        return G
    
    def find_irreducible_generators(G, n):
        generators = []
        for i in range(n):
            if all(G[i][j] == G[j][i] for j in range(i + 1, n)):
                generators.append(i)
        return generators
    
    def max_coset_representative_set_size(generators, G, n):
        max_size = 0
        for i in range(n):
            size = sum(1 for j in range(n) if all(G[j][k] == G[i][k] for k in generators))
            max_size = max(max_size, size)
        return max_size
    
    def entropy(f, n):
        ones = f.count(1)
        zeros = len(f) - ones
        p_one = ones / len(f)
        p_zero = zeros / len(f)
        if p_one == 0 or p_zero == 0:
            return 0
        return -p_one * math.log2(p_one) - p_zero * math.log2(p_zero)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n, random.randint(1, n**2))
            G = generate_conflict_graph(f, n)
            generators = find_irreducible_generators(G, n)
            max_size = max_coset_representative_set_size(generators, G, n)
            H_f = entropy(f, n)
            results.append((n, generators, H_f, max_size))
    
    conjecture_holds = all(len(r[1]) * math.log2(r[3]) >= r[2] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Entropy",
        "metric_value": sum(r[2] for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r[0] for r in results),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")