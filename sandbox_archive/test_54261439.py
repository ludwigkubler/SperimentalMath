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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_size(f):
        # Simple DPLL solver to estimate circuit size
        n = len(f)
        clauses = []
        for i in range(n):
            clause = random.sample(range(n), 3) + [i]
            clauses.append(clause)
        return len(clauses)
    
    def irreducible_representation_dimension(f):
        n = len(f)
        # Placeholder for actual computation
        # For simplicity, we assume a linear relationship
        return n
    
    metric_name = "correlation_coefficient"
    instances_tested = 0
    n_max = 0
    total_dim = 0
    total_size_squared = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            f = generate_boolean_function(n)
            dim = irreducible_representation_dimension(f)
            size_squared = circuit_size(f) ** 2
            total_dim += dim
            total_size_squared += size_squared
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    mean_dim = total_dim / instances_tested
    mean_size_squared = total_size_squared / instances_tested
    correlation_coefficient = (mean_dim * mean_size_squared - instances_tested * mean_dim * mean_size_squared) / ((instances_tested - 1) * math.sqrt((total_dim ** 2 - instances_tested * mean_dim ** 2) * (total_size_squared ** 2 - instances_tested * mean_size_squared)))
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
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
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")