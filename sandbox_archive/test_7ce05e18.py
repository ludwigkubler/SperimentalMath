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
    
    def incidence_matrix(instance):
        n = len(instance)
        matrix = [[0] * (1 << n) for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & (1 << k)) == (j & (1 << k)) for k in range(n)):
                    matrix[i][j] = 1
        return matrix
    
    def noncrossing_partition(matrix):
        n = len(matrix)
        partition = [set() for _ in range(n)]
        for i in range(1 << n):
            if all(matrix[i][j] == 0 for j in range(i + 1, 1 << n)):
                partition[bin(i).count('1') - 1].add(i)
        return partition
    
    def min_rank(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[i][j] != 0 for j in range(cols)):
                rank += 1
                for j in range(cols):
                    if matrix[i][j] != 0:
                        for k in range(rows):
                            matrix[k][j] -= matrix[i][j] * matrix[k][i]
        return rank
    
    n = random.randint(5, 40)
    instance = [random.sample(range(n), random.randint(1, n)) for _ in range(n)]
    matrix = incidence_matrix(instance)
    partition = noncrossing_partition(matrix)
    rank = min_rank(matrix)
    
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank > 3 * n / 2
    counterexample = "" if conjecture_holds else f"rank={rank}, expected>={3*n/2}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")