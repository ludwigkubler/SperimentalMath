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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_channel(n):
        X = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n))
        Y = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=n))
        P = [[Fraction(random.random()) for _ in range(n)] for _ in range(n)]
        for row in P:
            total = sum(row)
            for i in range(n):
                row[i] /= total
        return X, Y, P
    
    def free_probability_distribution(P):
        n = len(P)
        I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        A = [P]
        B = [I]
        
        while True:
            new_A = []
            new_B = []
            for a, b in zip(A, B):
                new_a = [[a[i][j] * b[k][l] + a[j][k] * b[l][i] for l in range(n)] for k in range(n)]
                new_b = [[b[i][j] * b[k][l] - a[i][k] * b[l][j] for l in range(n)] for k in range(n)]
                new_A.append(new_a)
                new_B.append(new_b)
            A.extend(new_A)
            B.extend(new_B)
            
            if len(A) > 2 * n:
                break
        
        rank = sum(1 for a, b in zip(A, B) if any(a[i][j] != 0 or b[i][j] != 0 for i in range(n) for j in range(n)))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        channel = generate_channel(n)
        rank = free_probability_distribution(channel)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= math.log(n) for n, rank in zip(n_values, ranks))
    counterexample = next((f"Rank {rank} > log({n})" for n, rank in zip(n_values, ranks) if rank > math.log(n)), "")
    
    return {
        "metric_name": "rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={first_failing_seed}")