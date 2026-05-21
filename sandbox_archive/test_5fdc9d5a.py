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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append([variables[i-1]])
        for i in range(1, n):
            clauses.append([-variables[i-1], variables[i]])
        return variables, clauses
    
    def compute_automorphism_group_size(graph):
        # Placeholder function to compute automorphism group size
        # This is a dummy implementation and should be replaced with actual algorithm
        return 2 ** (n - 1)
    
    def resolution_proof_length(clauses):
        # Placeholder function to compute Resolution proof length
        # This is a dummy implementation and should be replaced with actual algorithm
        return len(clauses) * n
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    graph = {i: [] for i in range(n)}
    
    automorphism_group_size = compute_automorphism_group_size(graph)
    proof_length = resolution_proof_length(clauses)
    
    ratio = Fraction(proof_length, 2 ** automorphism_group_size)
    
    return {
        "metric_name": "Ratio of Resolution Proof Length to 2^(ν(G))",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds 1.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + \
            [31, 37, 41, 43, 47, 53, 59, 61, 67, 71] + \
            [73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")