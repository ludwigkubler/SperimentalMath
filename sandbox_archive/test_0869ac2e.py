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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(m):
            clause = random.choice(variables)
            negate = random.choice([True, False])
            if negate:
                clause = f'¬{clause}'
            clauses.append(clause)
        return ' ∧ '.join(clauses), variables
    
    def hodge_integral(n, m, p):
        # Simplified Hodge integral calculation for demonstration
        return (n * m) % p
    
    def resolution_proof_length(n):
        # Simplified resolution proof length calculation for demonstration
        return 2 ** n
    
    p = 101  # Fixed prime for Hodge integral modulo operation
    c_p = 10  # Constant for the polynomial bound on Hodge integral
    
    results = []
    for _ in range(30):
        m = random.randint(5, 40)
        formula, variables = generate_tseitin_formula(len(variables), m)
        hodge_val = hodge_integral(len(variables), m, p)
        proof_length = resolution_proof_length(len(variables))
        
        if proof_length > c_p * m:
            return {
                "metric_name": "ResolutionProofLength",
                "metric_value": proof_length,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Formula: {formula}, Proof Length: {proof_length} > c_p * m = {c_p * m}"
            }
        
        results.append(hodge_val / c_p)
    
    mean_ratio = sum(results) / len(results)
    return {
        "metric_name": "HodgeIntegralRatio",
        "metric_value": mean_ratio,
        "instances_tested": 30,
        "conjecture_holds": mean_ratio <= 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= 1.1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r > 1.1 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > 1.1)
        print(f"RESULT: FALSIFIED counterexample=\"HodgeIntegralRatio > 1.1\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")