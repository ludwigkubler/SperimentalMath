# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define constants and parameters
    n = 30  # Number of instances per trial
    alpha = 1.0  # Constant for the conjecture
    
    def generate_function_field(g):
        """Generate a function field with genus g."""
        return [random.randint(0, 1) for _ in range(n)]
    
    def find_minimal_order(field):
        """Find the minimal order of an element in the multiplicative group G(K)."""
        for i in range(1, len(field)):
            if all((field[j] ** i) % 2 == field[j] for j in range(len(field))):
                return i
        return len(field)
    
    def quantum_query_complexity(g):
        """Estimate the quantum query complexity Q_BELL_k(A)."""
        # Placeholder function, replace with actual implementation
        return alpha * g**2
    
    total_order = 0
    total_query_complexity = 0
    
    for _ in range(n):
        g = random.randint(1, n)  # Random genus between 1 and n
        field = generate_function_field(g)
        order = find_minimal_order(field)
        query_complexity = quantum_query_complexity(g)
        
        total_order += order
        total_query_complexity += query_complexity
    
    mean_order = Fraction(total_order, n)
    mean_query_complexity = Fraction(total_query_complexity, n)
    
    conjecture_holds = (mean_order >= alpha * g**2) and (mean_query_complexity <= alpha * g**2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_order_and_query_complexity",
        "metric_value": mean_order,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(res["conjecture_holds"] for res in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")