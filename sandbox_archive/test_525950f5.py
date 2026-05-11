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
from math import factorial

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hook_length_formula(partition):
        n = sum(partition)
        numerator = factorial(n + 1)
        denominator = 1
        for row in partition:
            for cell, size in enumerate(row):
                denominator *= (cell + 1) * (size - cell)
        return numerator // denominator if denominator != 0 else float('inf')
    
    def determinant_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def communication_matrix(determinant):
        n = len(determinant)
        comm_matrix = []
        for i in range(n):
            row_sums = [sum(row[j] for j in range(i + 1)) for row in determinant]
            comm_matrix.append(row_sums)
        return comm_matrix
    
    def partition_from_matrix(matrix):
        n = len(matrix)
        sums = [sum(row) for row in matrix]
        sorted_sums = sorted(sums, reverse=True)
        partition = []
        current_sum = 0
        i = 0
        while current_sum < n:
            if sorted_sums[i] > 0:
                partition.append(sorted_sums[i])
                current_sum += sorted_sums[i]
                sorted_sums[i] = 0
            else:
                i += 1
        return partition
    
    def count_standard_young_tableaux(partition):
        return hook_length_formula(partition)
    
    n = random.randint(5, 40)
    determinant = determinant_matrix(n)
    comm_matrix = communication_matrix(determinant)
    det_partition = partition_from_matrix(determinant)
    comm_partition = partition_from_matrix(comm_matrix)
    
    det_tableau_count = count_standard_young_tableaux(det_partition)
    comm_tableau_count = count_standard_young_tableaux(comm_partition)
    
    ratio = comm_tableau_count / det_tableau_count
    conjecture_holds = ratio > 2**n
    
    return {
        "metric_name": "Ratio of Tableau Counts",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Det: {det_partition}, Comm: {comm_partition}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")