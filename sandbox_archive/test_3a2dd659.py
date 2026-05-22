# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def inversions_count(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count

def noncrossing_partitions(n):
    if n == 0:
        return [[]]
    partitions = []
    for k in range(1, n):
        for left in noncrossing_partitions(k):
            for right in noncrossing_partitions(n - k - 1):
                partitions.append([left + [i + k + 1] for i in left] + [right])
    return partitions

def minimal_rank(partition):
    n = len(partition)
    rank = 0
    for block in partition:
        rank += len(block) * (len(block) - 1) // 2
    return rank

def permutation_circuit_size(inversions):
    if inversions == 0:
        return 0
    phi_n = inversions_count([i + 1 for i in range(inversions)])
    if phi_n <= 0:
        return float('inf')  # Avoid log(0) or log(-ve)
    return phi_n * math.log2(phi_n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    permutation = [i + 1 for i in range(n)]
    random.shuffle(permutation)
    
    inversions = inversions_count(permutation)
    partition = noncrossing_partitions(n)[random.randint(0, len(noncrossing_partitions(n)) - 1)]
    rank = minimal_rank(partition)
    circuit_size = permutation_circuit_size(inversions)
    
    metric_value = rank
    conjecture_holds = (rank >= n**(2/3) and rank <= inversions * math.log2(inversions))
    counterexample = "" if conjecture_holds else f"Rank {rank} does not satisfy Ω(n^(2/3)) or O(φ(n) log^2 n)"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not satisfy Ω(n^(2/3)) or O(φ(n) log^2 n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")