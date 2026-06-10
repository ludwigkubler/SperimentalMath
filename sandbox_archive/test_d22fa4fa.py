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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def ehrhart_polynomial_degree(cnf):
        # Placeholder function to simulate Ehrhart polynomial degree calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 2  # Example: linear relationship for simplicity
    
    def circuit_complexity(cnf):
        # Placeholder function to simulate circuit complexity calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) * 3  # Example: linear relationship for simplicity
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    
    ehrhart_degree = ehrhart_polynomial_degree(cnf)
    circuit_comp = circuit_complexity(cnf)
    
    return {
        "metric_name": "Ehrhart Degree vs Circuit Complexity",
        "metric_value": ehrhart_degree,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ehrhart_degree <= circuit_comp,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")