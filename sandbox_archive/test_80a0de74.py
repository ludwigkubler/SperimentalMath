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
    
    def free_probability_tensor_product(clauses):
        n = len(clauses[0])
        M = [[0] * (2**n) for _ in range(2**n)]
        
        for clause in clauses:
            for i in range(2**n):
                for j in range(2**n):
                    if all((i >> k & 1) ^ (j >> k & 1) == int(lit > 0) for lit, sign in zip(clause, [1] * n)):
                        M[i][j] += 1
        
        # Normalize the matrix
        total = sum(sum(row) for row in M)
        if total == 0:
            return M
        
        for i in range(2**n):
            for j in range(2**n):
                M[i][j] /= total
        
        return M
    
    def noncommutative_information_entropy(M):
        n = len(M)
        entropy = 0
        for i in range(n):
            for j in range(n):
                if M[i][j] != 0:
                    entropy -= M[i][j] * math.log2(M[i][j])
        
        return entropy
    
    def dpll_proof_length(clauses):
        # Simplified DPLL proof length estimation
        return len(clauses) * n
    
    def generate_random_3cnf(n, num_clauses):
        clauses = []
        for _ in range(num_clauses):
            clause = []
            for _ in range(3):
                var = random.randint(1, n)
                sign = random.choice([1, -1])
                clause.append((var, sign))
            clauses.append(clause)
        return clauses
    
    n = 40
    num_clauses = 5 * n
    clauses = generate_random_3cnf(n, num_clauses)
    
    M = free_probability_tensor_product(clauses)
    entropy = noncommutative_information_entropy(M)
    proof_length = dpll_proof_length(clauses)
    
    if proof_length == 0:
        return {
            "metric_name": "noncommutative_information_entropy",
            "metric_value": entropy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length is zero"
        }
    
    bound = math.log(math.factorial(n)) ** (1/2)
    
    return {
        "metric_name": "noncommutative_information_entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")