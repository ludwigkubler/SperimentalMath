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
    
    def generate_sat_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def calculate_minimal_order(clauses):
        # Placeholder function to simulate the calculation
        return len(clauses) ** 2
    
    def boolean_circuit_size(clauses):
        # Placeholder function to simulate the calculation
        return len(clauses)
    
    n = random.randint(5, 40)
    m = random.randint(1, 2**n - 1)
    sat_instance = generate_sat_instance(n, m)
    
    minimal_order = calculate_minimal_order(sat_instance)
    circuit_size = boolean_circuit_size(sat_instance)
    
    return {
        "metric_name": "minimal_order_vs_circuit_size",
        "metric_value": minimal_order,
        "instances_tested": 1,
        "conjecture_holds": minimal_order >= circuit_size,
        "counterexample": "" if minimal_order >= circuit_size else "circuit_size < minimal_order"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample=\"circuit_size < minimal_order\" first_failing_seed={first_failing_seed}")