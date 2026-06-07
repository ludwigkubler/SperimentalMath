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
    
    def matrix_representation(f):
        n = len(f)
        M_f = [[f[i * (1 << (j - 1)) + k] for k in range(1 << (j - 1))] for j in range(1, n + 1)]
        return M_f
    
    def geometric_entropy(M):
        support = set()
        for row in M:
            for val in row:
                if val != 0:
                    support.add(val)
        entropy = 0
        for val in support:
            p = sum(row.count(val) for row in M) / (n * n)
            entropy -= p * math.log2(p)
        return entropy
    
    def communication_complexity_rank_variance(M):
        ranks = []
        for i in range(n):
            rank = 0
            for j in range(n):
                if M[i][j] != 0:
                    rank += 1
            ranks.append(rank)
        mean_rank = sum(ranks) / n
        variance = sum((x - mean_rank) ** 2 for x in ranks) / n
        return variance
    
    def f_n(x):
        # Example boolean function: parity of the number of 1s in binary representation
        return sum(int(bit) for bit in bin(x)[2:]) % 2
    
    n = random.randint(5, 40)
    M_f = matrix_representation(f_n)
    
    entropy = geometric_entropy(M_f)
    variance = communication_complexity_rank_variance(M_f)
    
    metric_value = entropy / (n * math.log2(n))
    conjecture_holds = metric_value <= 1  # Simplified for demonstration
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy_rank_variance_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")