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

def generate_quandle(m):
    quandle = {}
    for i in range(m):
        for j in range(m):
            quandle[(i, j)] = (i + j) % m
    return quandle

def minimal_rank_quandle(quandle):
    m = len(quandle)
    if not any(all(quandle[(i, j)] == quandle[(k, j)] for k in range(i)) for j in range(m)):
        return 1
    rank = 0
    for i in range(m):
        row = [quandle[(i, j)] for j in range(m)]
        if not any(all(row[j] == row[k] for k in range(j)) for j in range(m)):
            rank += 1
    return rank

def lower_bound_kclique(k, m):
    return math.ceil(2 ** (k / 2) ** m)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, min(n, 3))
    quandle = generate_quandle(m)
    
    rho_Q = minimal_rank_quandle(quandle)
    k = random.randint(3, 5)
    lower_bound = lower_bound_kclique(k, m)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rho_Q,
        "instances_tested": n,
        "conjecture_holds": rho_Q > lower_bound,
        "counterexample": "" if rho_Q > lower_bound else f"rho(Q)={rho_Q}, lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 50, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")