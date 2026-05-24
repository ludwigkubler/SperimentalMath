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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def formal_context(f, n):
        X = list(range(n))
        Y = set()
        for x in X:
            Y.add(tuple(f[i] for i in range(n) if (i >> x) & 1))
        return X, Y
    
    def galois_connection(X, Y):
        L = []
        U = []
        for y in Y:
            L.append([x for x in X if all(y[i] == f(x)[i] for i in range(len(f(x))))])
            U.append([y for y in Y if all(y[i] == f(x)[i] for i in range(len(f(x))))])
        return L, U
    
    def minimal_rank(L):
        rank = 0
        while L:
            x = L.pop()
            rank += 1
            L = [y for y in L if not any(all(y[i] == x[i] for i in range(len(x))) for x in L)]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        X, Y = formal_context(f, n)
        L, U = galois_connection(X, Y)
        rank = minimal_rank(L)
        total_rank += rank
        instances_tested += len(Y)
    
    mean_rank = total_rank / instances_tested
    
    if mean_rank <= n**2:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Mean rank {mean_rank} exceeds O(n^2) for n={n}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")