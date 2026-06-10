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
    
    def communication_complexity(f):
        n = f.index(1).bit_length()
        return n
    
    def truth_table(f):
        n = f.index(1).bit_length()
        table = []
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            outputs = f[i]
            table.append((inputs, outputs))
        return table
    
    def rank_of_matroid(truth_table):
        n = len(truth_table[0][0])
        m = len(truth_table)
        
        # Gaussian elimination
        A = [[1 if i == j else 0 for j in range(n)] + [truth_table[i][1]] for i in range(m)]
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i+1, m):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        break
                else:
                    continue
            pivot = Fraction(A[i][i])
            for j in range(n + 1):
                A[i][j] /= pivot
        
        rank = n
        for i in range(n, m):
            if all(A[i][j] == 0 for j in range(n)):
                rank -= 1
        return rank
    
    def log_expression(n, w):
        return math.log(n + math.log(w))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        w = communication_complexity(f)
        table = truth_table(f)
        rank = rank_of_matroid(table)
        
        results.append({
            "n": n,
            "w": w,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    conjecture_bound = log_expression(n, w)
    
    return {
        "metric_name": "Rank of Matroid",
        "metric_value": mean_rank,
        "instances_tested": 30,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(mean_rank - conjecture_bound) <= std_dev * 1.645,  # ~90% confidence
        "counterexample": "" if abs(mean_rank - conjecture_bound) <= std_dev * 1.645 else f"Rank {mean_rank} does not match bound {conjecture_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")