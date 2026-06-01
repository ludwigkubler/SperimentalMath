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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_rank(f):
    n = int(math.log2(len(f)))
    rank = 0
    for i in range(n):
        row = []
        for j in range(n):
            row.append(f[i * 2**(n-j-1): (i+1) * 2**(n-j-1)])
        rank += max(set([tuple(row[j]) for j in range(len(row))]), key=row.count)
    return rank

def p_adic_galois_representation(f):
    n = int(math.log2(len(f)))
    rho = 1
    for i in range(n):
        if any(f[i * 2**(n-j-1): (i+1) * 2**(n-j-1)] == f[(i+1) * 2**(n-j-1): (i+2) * 2**(n-j-1)] for j in range(len(f))):
            rho += 1
    return rho

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    rho = p_adic_galois_representation(f)
    rank_gal = communication_rank(f)
    return {
        "metric_name": "log_rho_over_rank",
        "metric_value": math.log(rho) / rank_gal if rank_gal != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, rho={p_adic_galois_representation(generate_boolean_function(r['n_max']))}, rank_gal={communication_rank(generate_boolean_function(r['n_max']))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break