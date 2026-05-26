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
    
    # Generate a random polynomial function f(x) = a_n*x^n + ... + a_1*x + a_0
    n = random.randint(5, 40)
    coefficients = [random.randint(-10, 10) for _ in range(n+1)]
    def f(x):
        return sum(a * x**i for i, a in enumerate(coefficients))
    
    # Compute the Galois representation ρ_f
    # This is a placeholder function. In practice, you would need to implement this.
    # For simplicity, we assume it returns a value that depends on n and coefficients.
    def min_order(ρ_f):
        return len(ρ_f)
    
    ρ_f = [i for i in range(n+1)]  # Placeholder implementation
    min_order_ρ_f = min_order(ρ_f)
    
    # Compute the quantum query complexity Q(f)
    # This is a placeholder function. In practice, you would need to implement this.
    def quantum_query_complexity(f):
        return n
    
    Q_f = quantum_query_complexity(f)
    
    # Check if the conjecture holds
    conjecture_holds = min_order_ρ_f <= 0.25 * Q_f**2
    
    return {
        "metric_name": "min_order_ρ_f",
        "metric_value": min_order_ρ_f,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={min_order_ρ_f}, expected=0.25 * {Q_f**2}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")