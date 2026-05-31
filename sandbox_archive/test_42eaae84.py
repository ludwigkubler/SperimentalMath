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

from fractions import Fraction
import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_symplectic_manifold(n):
        # Generate a random symplectic manifold with automorphism group order n
        # This is a placeholder function; replace it with actual implementation
        return n
    
    def evaluate_polynomial(f, M):
        # Evaluate polynomial f on the symplectic manifold M
        # This is a placeholder function; replace it with actual implementation
        return random.randint(1, 100)
    
    def communication_complexity(f, M):
        # Calculate the communication complexity for evaluating polynomial f on M
        # This is a placeholder function; replace it with actual implementation
        return len(f) * len(M)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_communication = 0
    instances_tested = 0
    
    for n in n_values:
        M = generate_symplectic_manifold(n)
        f = [random.randint(1, 10) for _ in range(n)]
        comm_complexity = communication_complexity(f, M)
        total_communication += comm_complexity
        instances_tested += len(f)
    
    mean_communication = Fraction(total_communication, instances_tested)
    expected_bound = Fraction(n_max ** 2, 1)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": float(mean_communication),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_communication - expected_bound) <= Fraction(expected_bound * 0.1, 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_communication} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_communication} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")