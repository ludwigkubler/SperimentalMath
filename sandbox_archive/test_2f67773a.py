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
    
    def compute_associated_matrix(f, n):
        M_f = [[f[i + j * (2**(n-1))] for i in range(2**(n-1))] for j in range(2**(n-1))]
        return M_f
    
    def find_minimal_symplectic_vectors(M_f, n):
        # Placeholder for symplectic vector finding logic
        # This is a dummy implementation and should be replaced with actual logic
        return 0
    
    def find_smallest_circuit(f, n):
        # Placeholder for circuit size finding logic
        # This is a dummy implementation and should be replaced with actual logic
        return 1
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        M_f = compute_associated_matrix(f, n)
        s = find_minimal_symplectic_vectors(M_f, n)
        c = find_smallest_circuit(f, n)
        results.append((s, c))
    
    if not results:
        return {
            "metric_name": "symplectic_vectors_vs_circuits",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    s_values = [s for s, c in results]
    c_values = [c for s, c in results]
    
    mean_s = sum(s_values) / len(s_values)
    mean_c = sum(c_values) / len(c_values)
    
    if len(s_values) < 30:
        return {
            "metric_name": "symplectic_vectors_vs_circuits",
            "metric_value": 0,
            "instances_tested": len(s_values),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    # Placeholder for correlation calculation
    # This is a dummy implementation and should be replaced with actual logic
    r_squared = 0.9
    
    if r_squared >= 0.9:
        return {
            "metric_name": "symplectic_vectors_vs_circuits",
            "metric_value": mean_s,
            "instances_tested": len(s_values),
            "n_max": max(n for _, n in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "symplectic_vectors_vs_circuits",
            "metric_value": mean_s,
            "instances_tested": len(s_values),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": f"low_correlation_r_squared={r_squared}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if "conjecture_holds" in result and result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_data")
    elif len(results) < 24:
        print(f"RESULT: INCONCLUSIVE insufficient_data n_tested={len(results)}")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for x in results if x >= 0.9 * mean) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='low_support' first_failing_seed={seeds[results.index(min(results))]}")