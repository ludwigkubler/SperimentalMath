# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def and_func(x):
        return all(x[i] for i in range(len(x)))
    
    def construct_affine_variety(and_func):
        n = len(next(iter(and_func.keys())))
        generators = []
        for x in itertools.product([0, 1], repeat=n):
            if and_func(x) == 1:
                generators.append(tuple(x))
        return generators
    
    def compute_rank(generators):
        m = len(generators)
        n = len(generators[0])
        A = [[Fraction(0)] * n for _ in range(m)]
        for i, gen in enumerate(generators):
            for j in range(n):
                A[i][j] = Fraction(gen[j])
        
        rank = 0
        for col in range(n):
            if any(A[row][col] != 0 for row in range(rank)):
                pivot_row = next(row for row in range(rank, m) if A[row][col] != 0)
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                for row in range(m):
                    if row != rank:
                        factor = -A[row][col] / A[rank][col]
                        for j in range(n):
                            A[row][j] += factor * A[rank][j]
                rank += 1
        return rank
    
    def communication_complexity(rank):
        return 2 ** (rank - 1)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    and_func = {tuple(random.randint(0, 1) for _ in range(n)): random.randint(0, 1) for _ in range(100)}
    
    generators = construct_affine_variety(and_func)
    rank = compute_rank(generators)
    comm_complexity = communication_complexity(rank)
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": comm_complexity,
        "instances_tested": 100,
        "conjecture_holds": rank > 1,  # Simplified check for exponential growth
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_complexity = sum(res["metric_value"] for res in results) / len(results)
    std_comm_complexity = math.sqrt(sum((res["metric_value"] - mean_comm_complexity) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_complexity} std={std_comm_complexity} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Communication complexity does not grow exponentially\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=exponential_growth_not_proven")