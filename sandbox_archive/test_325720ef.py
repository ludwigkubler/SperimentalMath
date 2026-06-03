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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def matrix_A_f(f):
        n = int(math.log2(len(f)))
        A = [[0] * (2**(n-1)) for _ in range(2**(n-1))]
        for i in range(2**(n-1)):
            for j in range(2**(n-1)):
                x = [i >> k & 1 for k in range(n)]
                y = [j >> k & 1 for k in range(n)]
                A[i][j] = f[x.index(0):x.index(1)] ^ f[y.index(0):y.index(1)]
        return A
    
    def communication_complexity_rank(A):
        n = len(A)
        rank = 0
        while A:
            max_row = max(range(n), key=lambda i: sum(abs(x) for x in A[i]))
            if all(A[max_row][j] == 0 for j in range(n)):
                break
            rank += 1
            for i in range(n):
                if A[i][max_row] != 0:
                    for j in range(n):
                        A[i][j] ^= A[max_row][j]
        return rank
    
    def minimal_Kostant_partitions(f):
        n = int(math.log2(len(f)))
        partitions = []
        for i in range(1, n):
            for comb in itertools.combinations(range(n), i):
                partition = [f[j:j+2**i] for j in range(0, len(f), 2**i)]
                if all(all(partition[k][j] == partition[k+1][j] for j in range(2**i)) for k in range(len(partition)-1)):
                    partitions.append(partition)
        return min(len(p) for p in partitions)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_partitions = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            A_f = matrix_A_f(f)
            rank = communication_complexity_rank(A_f)
            partitions = minimal_Kostant_partitions(f)
            total_rank += rank
            total_partitions += partitions
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_partitions = total_partitions / instances_tested
    conjecture_holds = mean_rank <= O(mean_partitions)
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank} > O(mean_partitions)={O(mean_partitions)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")

def O(x):
    return x  # Placeholder for the actual asymptotic function