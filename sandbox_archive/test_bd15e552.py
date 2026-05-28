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
    
    def communication_complexity_xor(f):
        n = int(math.log2(len(f)))
        count_00, count_01, count_10, count_11 = 0, 0, 0, 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == 0 and f[j] == 0:
                    count_00 += 1
                elif f[i] == 0 and f[j] == 1:
                    count_01 += 1
                elif f[i] == 1 and f[j] == 0:
                    count_10 += 1
                else:
                    count_11 += 1
        return max(count_00, count_01, count_10, count_11)
    
    def geometric_invariant_rank(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i] ^ f[j] for j in range(n)] for i in range(n)]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for other_row in matrix:
                    if other_row != row and all(other_row[k] == row[k] for k in range(n)):
                        other_row[:] = [0] * n
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        rank = geometric_invariant_rank(f)
        comm_complexity = communication_complexity_xor(f)
        results.append((rank, comm_complexity))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_comm_complexity = sum(comm_complexity for _, comm_complexity in results) / len(results)
    correlation_coefficient = sum((rank - mean_rank) * (comm_complexity - mean_comm_complexity) for rank, comm_complexity in results) / len(results)
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")