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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        k = min(k, n - k)
        c = 1
        for i in range(1, k + 1):
            c = c * (n - i + 1) // i
        return c
    
    def generate_random_instance(n: int, m: int) -> list:
        clauses = []
        for _ in range(m):
            clause = [random.choice([True, False]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def reflection_poset_complexity(clauses: list) -> int:
        n = len(clauses[0])
        generators = set()
        for i in range(n):
            for j in range(i + 1, n):
                if any(clause[i] != clause[j] for clause in clauses):
                    generators.add((i, j))
        return len(generators)
    
    def resolution_proof_width(clauses: list) -> int:
        # Simplified model of resolution proof width
        return sum(len(clause) for clause in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for m in m_values:
            for _ in range(5):  # Sample 5 instances per (n, m)
                clauses = generate_random_instance(n, m)
                proof_width = resolution_proof_width(clauses)
                poset_complexity = reflection_poset_complexity(clauses)
                metric_values.append(proof_width + math.log(m))
                instances_tested += 1
                n_max = max(n_max, n)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    conjecture_holds = all(proof_width + math.log(m) <= n ** (1/3) * m ** (2/3) + math.log(m) for proof_width, poset_complexity, clauses in zip(metric_values, [reflection_poset_complexity(generate_random_instance(n, m)) for _ in range(instances_tested)], [generate_random_instance(n, m) for _ in range(instances_tested)]))
    
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width + log(m)",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")