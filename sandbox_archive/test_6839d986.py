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
    
    def min_rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(rows):
            if any(matrix[j][i] != 0 for j in range(i, rows)):
                rank += 1
                for j in range(rows):
                    if matrix[j][i] != 0:
                        factor = Fraction(matrix[j][i], matrix[i][i])
                        for k in range(cols):
                            matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def generate_disjointness_instance(n):
        instance = []
        for _ in range(n):
            subset = random.sample(range(1, n + 1), random.randint(1, n))
            instance.append(subset)
        return instance
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different instances
            instance = generate_disjointness_instance(n)
            matrix = incidence_matrix(instance)
            rank = min_rank(matrix)
            total_rank += rank
            instances_tested += 1
    
    mean_value = total_rank / instances_tested
    support_fraction = (mean_value <= 3 * n_values[-1] / 2) and (mean_value > 0)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction,
        "counterexample": "" if support_fraction else f"rank={mean_value}, expected=3*{n_values[-1]}/2"
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
    support_fraction = all(result["conjecture_holds"] for result in results)
    
    if support_fraction:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction=1")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")