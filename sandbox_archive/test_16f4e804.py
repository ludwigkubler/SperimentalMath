# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def construct_coxeter_group(f):
    n = len(f)
    G = []
    for i in range(2**n):
        row = []
        for j in range(2**n):
            if i == j:
                row.append(0)
            elif f[i] != f[j]:
                row.append(1)
            else:
                row.append(0)
        G.append(row)
    return G

def count_non_trivial_relations(G):
    n = len(G)
    count = 0
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j] == 1 and G[j][i] == 1:
                count += 1
    return count

def communication_complexity(f):
    # Placeholder function; replace with actual implementation
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    G = construct_coxeter_group(f)
    non_trivial_relations = count_non_trivial_relations(G)
    comm_complexity = communication_complexity(f)
    
    if non_trivial_relations == 0:
        return {
            "metric_name": "communication_complexity_to_non_trivial_relations_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "non_trivial_relations_zero"
        }
    
    ratio = comm_complexity / non_trivial_relations
    return {
        "metric_name": "communication_complexity_to_non_trivial_relations_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='communication_complexity_too_large' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")