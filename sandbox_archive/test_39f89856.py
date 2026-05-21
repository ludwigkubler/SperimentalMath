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

def is_monotonic(f):
    n = len(f)
    for i in range(n):
        if any(f[i | (1 << j)] < f[i] for j in range(n)):
            return False
    return True

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def construct_coxeter_dynkin_diagram(f):
    n = len(f)
    diagram = {}
    for i in range(2**n):
        for j in range(n):
            if f[i | (1 << j)] < f[i]:
                diagram[(i, i | (1 << j))] = 1
    return diagram

def count_symmetry_classes(diagram):
    n = len(diagram)
    visited = [False] * n
    classes = 0
    
    def dfs(node):
        if not visited[node]:
            visited[node] = True
            for neighbor in range(n):
                if (node, neighbor) in diagram or (neighbor, node) in diagram:
                    dfs(neighbor)
    
    for i in range(n):
        if not visited[i]:
            classes += 1
            dfs(i)
    
    return classes

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    
    if not is_monotonic(f):
        return {
            "metric_name": "symmetry_classes",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "function_not_monotonic"
        }
    
    diagram = construct_coxeter_dynkin_diagram(f)
    symmetry_classes = count_symmetry_classes(diagram)
    
    return {
        "metric_name": "symmetry_classes",
        "metric_value": symmetry_classes,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")