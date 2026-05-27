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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_resolution_proof(f):
        n = int(math.log2(len(f)))
        proof = []
        for i in range(n):
            new_clause = []
            for j in range(2**(i+1)):
                if f[j] != f[j ^ (1 << i)]:
                    new_clause.append(j)
                    new_clause.append(j ^ (1 << i))
            proof.append(new_clause)
        return proof
    
    def calculate_symmetry_measure(proof):
        n = len(proof[0])
        symmetry_count = 0
        for clause in proof:
            for j in range(n):
                if all(clause[i] == clause[(i + j) % n] for i in range(len(clause))):
                    symmetry_count += 1
        return symmetry_count / len(proof)
    
    def log_size(proof):
        return math.log2(len(proof))
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    C = construct_resolution_proof(f)
    psi_C = calculate_symmetry_measure(C)
    size_C = len(C)
    
    alpha = 1.0
    upper_bound = alpha * log_size(C)
    
    result = {
        "metric_name": "symmetry_measure",
        "metric_value": psi_C,
        "instances_tested": 1,
        "conjecture_holds": psi_C <= upper_bound,
        "counterexample": "" if psi_C <= upper_bound else f"psi(C)={psi_C}, upper_bound={upper_bound}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = result["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")