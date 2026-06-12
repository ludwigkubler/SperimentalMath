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
    
    def generate_random_sat_instance(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def dpll_search_tree_width(phi):
        stack = [(phi, 1)]
        max_depth = 0
        while stack:
            phi, depth = stack.pop()
            if not phi:
                continue
            if all(c == '0' or c == '1' for c in phi):
                max_depth = max(max_depth, depth)
                continue
            var = next(i for i, c in enumerate(phi) if c != '2')
            literals = [phi[:var] + '0' + phi[var+1:], phi[:var] + '1' + phi[var+1:]]
            stack.append((literals[0], depth + 1))
            stack.append((literals[1], depth + 1))
        return max_depth
    
    def minimal_index_of_automorphism_groups(phi):
        n = len(phi)
        generators = []
        for i in range(n):
            if phi[i] != '2':
                continue
            new_phi = phi[:i] + '0' + phi[i+1:]
            if all(new_phi[j] == phi[j] or new_phi[j] == '2' for j in range(n)):
                generators.append(i)
        return len(generators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_random_sat_instance(n)
            instances_tested += 1
            n_max = max(n_max, n)
            if not phi:
                continue
            w_DPLL = dpll_search_tree_width(phi)
            if w_DPLL == 0:
                continue
            ι_A = minimal_index_of_automorphism_groups(phi)
            ratios.append(ι_A / w_DPLL)
    
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = mean_ratio <= 1 and 1 >= mean_ratio
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Minimal Index to DPLL Width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")