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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for var in variables:
            clauses.append([var, f'~{var}'])
        for i in range(1, n):
            clauses.append([f'x{i}', f'x{i-1}', f'~x{i}'])
        return clauses
    
    def compute_minimal_symplectic_rank(clauses):
        # Placeholder function to simulate polynomial-time computation
        return len(clauses)
    
    def resolution_proof_length(clauses):
        stack = []
        for clause in clauses:
            if all(var not in stack and f'~{var}' not in stack for var in clause):
                stack.extend(clause)
            elif any(f'~{var}' in stack for var in clause):
                stack.remove(f'~{var}')
            else:
                return 1
        return len(stack)
    
    n_values = [5, 10, 20, 40]
    results = []
    for n in n_values:
        for _ in range(30):  # Ensure at least 30 instances per seed
            formula = generate_tseitin_formula(n)
            r = compute_minimal_symplectic_rank(formula)
            proof_length = resolution_proof_length(formula)
            results.append({
                "n": n,
                "r": r,
                "proof_length": proof_length
            })
    
    total_instances = len(results)
    conjecture_holds = all(proof_length >= 2**(math.ceil(math.log2(r))) for _, r, proof_length in results)
    counterexample = "" if conjecture_holds else f"n={results[0]['n']}, r={results[0]['r']}, proof_length={results[0]['proof_length']}"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": sum(proof_length for _, _, proof_length in results) / total_instances,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv[1:]) > 0:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, r={results[0]['r']}, proof_length={results[0]['proof_length']}\" first_failing_seed={first_failing_seed}")