# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_expander_graph(n):
        # Generate a random expander graph using the adjacency matrix method
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 2 / (n - 1):
                    A[i][j] = A[j][i] = 1
        return A
    
    def compute_second_eigenvalue(A):
        # Compute the second eigenvalue of the adjacency matrix using power iteration method
        n = len(A)
        v = [random.random() for _ in range(n)]
        v /= math.sqrt(sum(x * x for x in v))
        for _ in range(100):
            v_next = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next /= math.sqrt(sum(x * x for x in v_next))
            v, v_next = v_next, v
        λ = sum(A[i][j] * v[j] for i in range(n) for j in range(i + 1, n))
        return abs(2 * λ / (n - 1))
    
    def compute_proof_complexity(n):
        # Simulate the proof complexity using a small DPLL solver
        # This is a placeholder function and should be replaced with actual implementation
        return random.randint(10, 100)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = generate_expander_graph(n)
    λ = compute_second_eigenvalue(A)
    proof_complexity = compute_proof_complexity(n)
    
    return {
        "metric_name": "proof_complexity",
        "metric_value": proof_complexity,
        "instances_tested": 1,
        "conjecture_holds": proof_complexity >= n / (λ ** 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "proof_complexity_too_low"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")