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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(min(m, n)):
            if abs(A[i][i]) > 1e-9:
                r += 1
        return r
    
    def circuit_depth(n, q):
        # Simplified model of circuit depth for modular sums
        return math.ceil(math.log2(q) + math.log2(n))
    
    def generate_curve(q):
        # Simplified generation of an algebraic curve over F_q
        return [random.randint(0, q-1) for _ in range(random.randint(5, 10))]
    
    def hodge_class_rank(curve):
        # Simplified model of Hodge class rank for a curve
        return len(set(curve))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    q = random.randint(2, 10)
    curve = generate_curve(q)
    h_rank = hodge_class_rank(curve)
    depth = circuit_depth(n, q)
    
    if h_rank > c * depth:
        counterexample = f"Curve: {curve}, Hodge Rank: {h_rank}, Depth: {depth}"
        return {
            "metric_name": "Hodge Rank / Circuit Depth",
            "metric_value": h_rank / depth,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": counterexample
        }
    
    return {
        "metric_name": "Hodge Rank / Circuit Depth",
        "metric_value": h_rank / depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")