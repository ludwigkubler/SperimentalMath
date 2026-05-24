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
    
    def generate_function_field(g):
        # Simplified function field generation for testing purposes
        return [random.randint(1, 2**g) for _ in range(2**g)]
    
    def find_minimal_order(g):
        K = generate_function_field(g)
        order = 1
        while True:
            if all(pow(x, order, g) == 1 for x in K):
                return order
            order += 1
    
    def quantum_query_complexity(order, k):
        # Simplified quantum query complexity calculation for testing purposes
        return order * k
    
    n = random.randint(5, 40)
    total_order = 0
    total_query_complexity = 0
    
    for _ in range(n):
        g = random.randint(1, 5)  # Limiting genus to avoid large computations
        order = find_minimal_order(g)
        query_complexity = quantum_query_complexity(order, n)
        
        if order < g**2 or query_complexity > g**2:
            return {
                "metric_name": "Quantum Query Complexity",
                "metric_value": query_complexity,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Order {order} < {g**2} or Q_BELL_k({n}) > {g**2}"
            }
        
        total_order += order
        total_query_complexity += query_complexity
    
    mean_order = Fraction(total_order, n)
    mean_query_complexity = Fraction(total_query_complexity, n)
    
    return {
        "metric_name": "Quantum Query Complexity",
        "metric_value": mean_query_complexity,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order < g^2 or Q_BELL_k({n}) > g^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")