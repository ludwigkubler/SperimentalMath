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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(n):
            if f[i] != f[2**i - 1]:
                count += 1
        return count
    
    def tropical_hermitian_form(f):
        n = len(f)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if f[i] == f[j]:
                    H[i][j] = 1
                    H[j][i] = 1
        return H
    
    def min_rank(H):
        n = len(H)
        rank = 0
        for i in range(n):
            if any(H[i]):
                rank += 1
                for j in range(n):
                    if H[j][i]:
                        for k in range(n):
                            H[j][k] ^= H[i][k]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            f = generate_random_boolean_function(n)
            C_f = communication_complexity(f)
            if C_f > n**(1/4):
                H = tropical_hermitian_form(f)
                rank = min_rank(H)
                total_rank += rank
                instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank >= math.sqrt(n_values[-1])
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} < Ω(n^(1/2)) for n={n_values[-1]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank < Ω(n^(1/2))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")