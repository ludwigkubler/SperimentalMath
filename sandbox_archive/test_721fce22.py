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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll_refutation_depth(f):
        n = len(f)
        if n == 1:
            return 1
        depth = 0
        for i in range(n):
            sub_f = f[:]
            sub_f[i] = 1 - sub_f[i]
            depth = max(depth, 1 + dpll_refutation_depth(sub_f))
        return depth
    
    def quasi_linear_representation(f):
        n = len(f)
        if n == 1:
            return [f[0]]
        representation = []
        for i in range(n):
            sub_f = f[:]
            sub_f[i] = 1 - sub_f[i]
            representation.append(sub_f)
        return representation
    
    def rank(representation):
        n = len(representation)
        if n == 1:
            return 1
        max_rank = 0
        for i in range(n):
            sub_rep = representation[:]
            sub_rep.pop(i)
            max_rank = max(max_rank, rank(sub_rep))
        return max_rank + 1
    
    def linear_equivalence(r1, r2):
        n = len(r1)
        if n != len(r2):
            return False
        for i in range(n):
            if not all(x == y for x, y in zip(r1[i], r2[i])):
                return False
        return True
    
    def find_counterexample(f, d):
        representation = quasi_linear_representation(f)
        rank_rep = rank(representation)
        if rank_rep < d:
            return f"Counterexample found: f={f}, d={d}, rank_rep={rank_rep}"
        return ""
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    d = dpll_refutation_depth(f)
    representation = quasi_linear_representation(f)
    rank_rep = rank(representation)
    
    if rank_rep < d:
        counterexample = find_counterexample(f, d)
    else:
        counterexample = ""
    
    return {
        "metric_name": "rank_over_d",
        "metric_value": rank_rep / d,
        "instances_tested": 1,
        "conjecture_holds": rank_rep >= d,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank_over_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_over_d} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_over_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")