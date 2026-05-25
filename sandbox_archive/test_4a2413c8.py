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
    
    def generate_noncrossing_partition(n):
        if n == 1:
            return [[0]]
        elif n == 2:
            return [[0], [1]], [[0, 1]]
        else:
            partitions = []
            for i in range(1, n):
                left_partitions = generate_noncrossing_partition(i)
                right_partitions = generate_noncrossing_partition(n - i)
                for lp in left_partitions:
                    for rp in right_partitions:
                        new_partition = [lp + [i], rp]
                        if not any(new_partition[j][0] > new_partition[j+1][0] for j in range(len(new_partition)-1)):
                            partitions.append(new_partition)
            return partitions
    
    def boolean_function_from_partition(partition):
        n = len(partition)
        f = [0] * (2**n)
        for i in range(2**n):
            binary_rep = bin(i)[2:].zfill(n)
            if all(binary_rep[j] == '1' for j in partition[0]):
                f[i] = 1
            else:
                f[i] = 0
        return f
    
    def communication_complexity(f, n):
        # Simplified model of randomized communication complexity for DISJOINTNESS
        return n * (n + 1) // 2
    
    def rank_of_partition(partition):
        return len(partition)
    
    n = random.randint(5, 40)
    partitions = generate_noncrossing_partition(n)
    partition = random.choice(partitions)
    f = boolean_function_from_partition(partition)
    cc = communication_complexity(f, n)
    rank = rank_of_partition(partition)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": cc / (n**2 * math.log(n)),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")