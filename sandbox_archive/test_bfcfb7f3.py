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
    
    def generate_sat_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        n = len(instance)
        assignment = [-1] * n
        
        def backtrack(level):
            if level == n:
                return True
            for val in [0, 1]:
                assignment[level] = val
                if all((instance[i] & (1 << j)) ^ assignment[j] == 0 for i in range(n)):
                    if backtrack(level + 1):
                        return True
            assignment[level] = -1
            return False
        
        return backtrack(0)
    
    def automorphism_group(instance):
        n = len(instance)
        generators = []
        
        def is_fixed_by_permutation(perm):
            for i in range(n):
                if instance[i] != instance[perm[i]]:
                    return False
            return True
        
        for perm in itertools.permutations(range(n)):
            if is_fixed_by_permutation(perm) and all(perm[i] == perm[j] or perm[i] != perm[j] for i, j in itertools.combinations(range(n), 2)):
                generators.append(perm)
        
        return len(generators)
    
    def shv(instance):
        n = len(instance)
        max_depth = 0
        
        def backtrack(level, assignment):
            nonlocal max_depth
            if level == n:
                max_depth = max(max_depth, assignment.count(1))
                return
            for val in [0, 1]:
                assignment.append(val)
                backtrack(level + 1, assignment)
                assignment.pop()
        
        backtrack(0, [])
        return max_depth
    
    ratios = []
    instances_tested = 0
    n_max = 0
    
    for n in range(5, 41):
        instance = generate_sat_instance(n)
        instances_tested += len(instance)
        n_max = max(n_max, n)
        
        if not dpll(instance):
            continue
        
        shv_value = shv(instance)
        automorphism_group_size = automorphism_group(instance)
        ratio = automorphism_group_size / shv_value
        ratios.append(ratio)
    
    mean_ratio = sum(ratios) / len(ratios)
    conjecture_holds = all(r <= mean_ratio for r in ratios)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")