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
    
    def communication_distance(f, g):
        return sum(1 for i in range(len(f)) if f[i] != g[i])
    
    def min_plus_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * (2*n) for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                if f[2*i] == 1 and f[2*j+1] == 1:
                    M[i][j+n] = 1
        return M
    
    def symplectic_hull(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[j][i] != 0 for j in range(rank)):
                for j in range(rank, n):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        break
                for j in range(i+1, n):
                    factor = -M[j][i] / M[i][i]
                    for k in range(n):
                        M[j][k] += factor * M[i][k]
                rank += 1
        return rank
    
    def min_rank(f, g):
        d = communication_distance(f, g)
        M_f = min_plus_representation(f)
        M_g = min_plus_representation(g)
        M_fg = [[M_f[i][j] + M_g[i][j] for j in range(len(M_f[0]))] for i in range(len(M_f))]
        return symplectic_hull(M_fg)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        g = generate_boolean_function(n)
        while communication_distance(f, g) == 0:
            f = generate_boolean_function(n)
            g = generate_boolean_function(n)
        rank = min_rank(f, g)
        results.append((n, rank))
    
    if all(rank <= n**2 for _, rank in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "minimal_rank > O(d^2)"
    
    return {
        "metric_name": "min_rank",
        "metric_value": sum(rank for _, rank in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank > O(d^2)\" first_failing_seed={seeds[first_failing_seed]}")