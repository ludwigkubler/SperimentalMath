# auto-injected by SEC sandbox
import math
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
import sys
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def formal_context(f, n):
        X = list(range(2**n))
        Y = list(range(len(f)))
        return X, Y
    
    def galois_connection(X, Y):
        L = []
        U = []
        for x in X:
            L.append([y for y in Y if all(x & (1 << i) == f(y)[i] for i in range(n))])
        for y in Y:
            U.append([x for x in X if all(x & (1 << i) == f(y)[i] for i in range(n))])
        return L, U
    
    def minimal_rank(L):
        rank = 0
        while L:
            rank += 1
            new_L = []
            for l in L:
                if not any(l[i].issubset(new_l) for i, new_l in enumerate(new_L)):
                    new_L.append(l)
            L = new_L
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        X, Y = formal_context(f, n)
        L, U = galois_connection(X, Y)
        rank = minimal_rank(L)
        total_rank += rank
        instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = mean_rank <= n**2
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank} exceeds O(n^2)"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")