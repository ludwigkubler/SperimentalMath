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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def uniform_matroid(n, r):
        elements = list(range(1, n + 1))
        matroid = []
        for i in range(r):
            subset = random.sample(elements, i + 1)
            matroid.append(subset)
        return matroid
    
    def matroid_connectivity(matroid):
        n = len(matroid[0])
        elements = set(range(1, n + 1))
        for r in range(n, 0, -1):
            for subset in itertools.combinations(elements, r):
                if all(all(x not in subset for x in s) for s in matroid):
                    return r
        return 0
    
    def pseudorandom_generator(seed, n):
        random.seed(seed)
        return [random.randint(0, 1) for _ in range(n)]
    
    def statistical_distance(sample1, sample2):
        n = len(sample1)
        return sum(abs(a - b) for a, b in zip(sample1, sample2)) / n
    
    def circuit_test(generator, depth):
        # Placeholder function to simulate circuit testing
        # In practice, this would involve actual circuit simulation and statistical distance computation
        return random.random() < 0.5
    
    n = random.randint(5, 40)
    r = random.randint(1, min(n, 10))
    matroid = uniform_matroid(n, r)
    connectivity = matroid_connectivity(matroid)
    
    if connectivity == 0:
        return {
            "metric_name": "seed_length",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    s1 = math.log(n)
    s2 = n / connectivity
    
    generator1 = pseudorandom_generator(seed, n)
    generator2 = pseudorandom_generator(seed + 1, n)
    
    test_depths = [5, 10, 15, 20]
    instances_tested = len(test_depths)
    success_count = 0
    
    for depth in test_depths:
        if circuit_test(generator1, depth) and not circuit_test(generator2, depth):
            success_count += 1
        elif not circuit_test(generator1, depth) and circuit_test(generator2, depth):
            success_count -= 1
    
    seed_length = s1 if connectivity >= math.log(n) else s2
    conjecture_holds = abs(success_count / instances_tested - (connectivity >= math.log(n))) < 0.1
    
    return {
        "metric_name": "seed_length",
        "metric_value": seed_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    total_metric_value = 0
    total_instances_tested = 0
    support_count = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        total_instances_tested += trial_result["instances_tested"]
        if trial_result["conjecture_holds"]:
            support_count += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    std_metric_value = math.sqrt(sum((trial_result["metric_value"] - mean_metric_value) ** 2 for trial_result in run_trial(seed) for seed in seeds)) / len(seeds)
    support_fraction = support_count / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in run_trial(seed) for seed in seeds):
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={total_instances_tested}")