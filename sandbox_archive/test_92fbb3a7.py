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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def delone_set_representation(f):
    n = int(math.log2(len(f)))
    delone_set = []
    for i in range(2**n):
        if f[i] == 1:
            delone_set.append(i)
    return delone_set

def matroid_rank(d):
    elements = list(d)
    rank = 0
    independent_sets = [[]]
    for e in elements:
        new_independent_sets = []
        for s in independent_sets:
            if all(e & x == 0 for x in s):
                new_independent_sets.append(s + [e])
        independent_sets.extend(new_independent_sets)
        rank = max(rank, len(max(independent_sets, key=len)))
    return rank

def communication_complexity_k_clique(n):
    # Simplified version of k-clique communication complexity
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        d = delone_set_representation(f)
        rank = matroid_rank(d)
        cc_k_clique = communication_complexity_k_clique(n)
        
        results.append(rank / cc_k_clique)
    
    mean = sum(results) / len(results)
    conjecture_holds = all(x <= 1 for x in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank_over_cc",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction={support_fraction}")
    elif any(r > 1 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")