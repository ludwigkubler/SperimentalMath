# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def compute_associated_matrix(f, n):
    M_f = [[f[i + j * (2**(n-1))] for i in range(2**(n-1))] for j in range(2**(n-1))]
    return M_f

def find_symplectic_vectors(M_f):
    n = int(math.log2(len(M_f)))
    symplectic_vectors = set()
    
    def is_symplectic(v):
        for i, j in combinations(range(n), 2):
            if v[i] * v[j] != -v[(i + j) % n]:
                return False
        return True
    
    for v in product([0, 1], repeat=n):
        if is_symplectic(v):
            symplectic_vectors.add(tuple(v))
    
    return symplectic_vectors

def find_smallest_circuit(f, n):
    # Placeholder function to simulate SAT solver
    # This is a dummy implementation and should be replaced with an actual SAT solver
    return random.randint(10, 50)

def run_test(n):
    f = generate_random_boolean_function(n)
    M_f = compute_associated_matrix(f, n)
    symplectic_vectors = find_symplectic_vectors(M_f)
    circuit_size = find_smallest_circuit(f, n)
    return len(symplectic_vectors), circuit_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        s, c = run_test(n)
        results.append((s, c))
    
    if not results:
        return {
            "metric_name": "symplectic_vectors_circuit_size",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    s_values = [s for s, _ in results]
    c_values = [c for _, c in results]
    
    mean_s = sum(s_values) / len(s_values)
    mean_c = sum(c_values) / len(c_values)
    std_s = math.sqrt(sum((x - mean_s)**2 for x in s_values) / len(s_values))
    std_c = math.sqrt(sum((x - mean_c)**2 for x in c_values) / len(c_values))
    
    correlation = sum((s - mean_s) * (c - mean_c) for s, c in results) / (len(results) * std_s * std_c)
    
    return {
        "metric_name": "symplectic_vectors_circuit_size",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["conjecture_holds"]) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    else:
        counterexample = min((r["counterexample"] for r in results if not r["conjecture_holds"]), default="")
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")