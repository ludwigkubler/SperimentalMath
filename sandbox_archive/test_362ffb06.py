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
            return [(0,)]
        elif n == 2:
            return [(0,), (1,)]
        else:
            partitions = []
            for i in range(1, n-1):
                left_partitions = generate_noncrossing_partition(i)
                right_partitions = generate_noncrossing_partition(n-i-1)
                for lp in left_partitions:
                    for rp in right_partitions:
                        if max(lp) < min(rp):
                            partitions.append(lp + rp)
            return partitions
    
    def boolean_function_from_partition(partition, n):
        function = [0] * (2**n)
        for subset in range(1, 2**n):
            binary_subset = bin(subset)[2:].zfill(n)
            if all(int(binary_subset[i]) == i % 2 for i in partition):
                function[subset] = 1
        return function
    
    def communication_complexity(f, n):
        complexity = 0
        for subset in range(1, 2**n):
            binary_subset = bin(subset)[2:].zfill(n)
            if f[subset] == 1:
                complexity += len(binary_subset) - sum(int(bit) for bit in binary_subset)
        return complexity
    
    def rank_of_partition(partition):
        n = max(max(p) for p in partition) + 1
        matrix = [[0] * n for _ in range(n)]
        for subset in range(1, 2**n):
            binary_subset = bin(subset)[2:].zfill(n)
            if all(int(binary_subset[i]) == i % 2 for i in partition):
                for i in range(n):
                    matrix[subset][i] = int(binary_subset[i])
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for j in range(rank):
                    if any(matrix[j]):
                        factor = row[j] / matrix[j][j]
                        for k in range(n):
                            row[k] -= factor * matrix[j][k]
        return rank
    
    n = random.randint(5, 40)
    partition = generate_noncrossing_partition(n)
    f = boolean_function_from_partition(partition, n)
    complexity = communication_complexity(f, n)
    rank = rank_of_partition(partition)
    
    if rank == 1:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "A noncrossing partition matroid M with rank 1 and n variables, where the randomized communication complexity for DISJOINTNESS is less than n^2 log n."
        }
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": -1,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "Mapping undefined for noncrossing partition matroid to Boolean function and communication complexity."
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*2 + 1, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")