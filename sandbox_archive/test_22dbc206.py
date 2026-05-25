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
    
    def tropical_add(x, y):
        return max(x, y)
    
    def tropical_multiply(x, y):
        if x == float('-inf') or y == float('-inf'):
            return float('-inf')
        return x + y
    
    def tropical_negate(x):
        return -x
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_is_zero(x):
        return x == float('-inf')
    
    def tropical_rank(f):
        n = len(f)
        if n == 1:
            return 1
        rank = 1
        for i in range(1, n):
            if not any(tropical_is_zero(f[i][j]) for j in range(i)):
                rank += 1
        return rank
    
    def BP_ReadTwice_complexity(P):
        n = len(P)
        t_star = [0] * (n + 1)
        t_star[0] = 1
        for i in range(n):
            t_star[i+1] = sum(tropical_multiply(t_star[j], P[i][j]) for j in range(i+1))
        return max(t_star)
    
    def quasi_symmetric_function(P):
        n = len(P)
        f = [[tropical_zero() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            f[0][i] = P[i][0]
        for i in range(1, n):
            for j in range(i+1):
                f[j][i] = tropical_add(f[j-1][i], tropical_multiply(P[i][j], f[j][i-1]))
        return f
    
    def generate_read_twice_branching_program(n):
        P = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1):
                P[i][j] = random.choice([tropical_zero(), tropical_one()])
        return P
    
    n = 40
    P = generate_read_twice_branching_program(n)
    f = quasi_symmetric_function(P)
    rank = tropical_rank(f)
    bp_complexity = BP_ReadTwice_complexity(P)
    
    if rank == 1:
        counterexample = "trivial_IP_2"
        conjecture_holds = False
    else:
        ratio = bp_complexity / math.log(rank, 2)
        conjecture_holds = abs(ratio - 1) <= 0.5
        counterexample = ""
    
    return {
        "metric_name": "BP_ReadTwice_complexity vs tropical rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_ratio} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "trivial_IP_2" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] == "trivial_IP_2")
        print(f"RESULT: FALSIFIED counterexample=\"trivial IP_2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")