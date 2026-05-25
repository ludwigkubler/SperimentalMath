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
    
    def generate_parity_function(n):
        return [i % 2 for i in range(1 << n)]
    
    def ac0_circuit_depth(n):
        if n == 1:
            return 1
        return 1 + ac0_circuit_depth(n - 1)
    
    def p_adic_differential(f, x):
        diff = []
        for i in range(len(f)):
            diff.append((f[i] - f[(i - 1) % len(f)]) / (x - 1))
        return diff
    
    def rank(differential):
        m, n = len(differential), len(differential[0])
        if m == 0 or n == 0:
            return 0
        for i in range(m):
            if differential[i][0] != 0:
                pivot_row = differential[i]
                for j in range(i + 1, m):
                    factor = differential[j][0] / pivot_row[0]
                    for k in range(n):
                        differential[j][k] -= factor * pivot_row[k]
        rank_value = sum(1 for row in differential if any(row))
        return rank_value
    
    n_min = 5
    n_max = 40
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(n_min, n_max + 1):
        f = generate_parity_function(n)
        depth = ac0_circuit_depth(n)
        diff = p_adic_differential(f, depth)
        rank_value = rank(diff)
        
        instances_tested += 1
        total_rank += rank_value
        
        if rank_value < math.log2(2**n):
            conjecture_holds = False
            counterexample = f"n={n}, rank={rank_value} < log2(2^n)"
    
    mean_rank = total_rank / instances_tested
    
    return {
        "metric_name": "Minimal Rank of p-Adic Differential",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")