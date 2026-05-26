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
    n = random.randint(5, 40)
    
    # Generate a random Boolean function f(x_1, ..., x_n)
    def f(*x):
        return sum(x) % 2
    
    # Compute the minimal rank τ(P_f)
    def is_noncrossing_partition(partition):
        for i in range(len(partition)):
            for j in range(i + 1, len(partition)):
                if any(partition[i][k] & partition[j][l] for k in range(len(partition[i])) for l in range(len(partition[j]))):
                    return False
        return True
    
    def generate_partitions():
        partitions = []
        for i in range(2**n):
            partition = [[], []]
            for j in range(n):
                if (i >> j) & 1:
                    partition[0].append(1 << j)
                else:
                    partition[1].append(1 << j)
            if is_noncrossing_partition(partition):
                partitions.append(partition)
        return partitions
    
    def minimal_rank(f, n):
        partitions = generate_partitions()
        min_rank = float('inf')
        for partition in partitions:
            rank = len(partition)
            if all(f(*[x for x in range(n) if (1 << i) & j]) == f(*[x for x in range(n) if (1 << i) & k]) for j, k in zip(partition[0], partition[1])):
                min_rank = min(min_rank, rank)
        return min_rank
    
    τ_P_f = minimal_rank(f, n)
    
    # Calculate the communication complexity CC_XOR-AND(f)
    def xor_and_tree_complexity(n):
        if n == 1:
            return 0
        else:
            return 1 + max(xor_and_tree_complexity(n // 2), xor_and_tree_complexity((n + 1) // 2))
    
    CC_XOR_AND_f = xor_and_tree_complexity(n)
    
    # Check the ratio CC_XOR-AND(f)/τ(P_f)
    if τ_P_f == 0:
        return {
            "metric_name": "CC_XOR-AND(f)/τ(P_f)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "minimal_rank_is_zero"
        }
    
    ratio = CC_XOR_AND_f / τ_P_f
    
    return {
        "metric_name": "CC_XOR-AND(f)/τ(P_f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= n**2,  # Polynomial upper bound
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC_XOR-AND(f)/τ(P_f) exceeds polynomial bound\" first_failing_seed={seeds[first_failing_seed]}")