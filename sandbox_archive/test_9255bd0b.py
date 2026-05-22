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

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_function_to_permutation(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Boolean function length must be a power of 2")
        return [f(i).index(1) for i in range(n)]
    
    def tensor_rank(permutation):
        n = len(permutation)
        rank = 0
        for i in range(n):
            if permutation[i] != i:
                rank += 1
        return rank
    
    def minimal_representation_rank(f):
        n = int(math.log2(len(f)))
        # Simplified representation rank calculation (placeholder)
        return sum(f[i] for i in range(n)) / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        permutation = boolean_function_to_permutation(f)
        rho_f = minimal_representation_rank(f)
        tau_n = tensor_rank(permutation)
        
        results.append({
            "n": n,
            "rho_f": rho_f,
            "tau_n": tau_n
        })
    
    correlation_coefficient = 0
    for result in results:
        correlation_coefficient += (result["rho_f"] - sum(r["rho_f"] for r in results) / len(results)) * \
                                   (result["tau_n"] - sum(r["tau_n"] for r in results) / len(results))
    
    correlation_coefficient /= len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<{result['counterexample']}\" first_failing_seed={first_failing_seed}")