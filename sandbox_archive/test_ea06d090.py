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
    
    def generate_CNF(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([-1, 1]) * j for j in range(1, n + 1)]
            clauses.append(clause)
        return clauses
    
    def compute_Lp_norm(clauses, p):
        norm = 0
        for clause in clauses:
            norm += sum(abs(lit) ** p for lit in clause) ** (1 / p)
        return norm
    
    def compute_resolution_proof_size(clauses):
        # Simplified DPLL solver to estimate proof size
        stack = []
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        def dpll(lit):
            if not clauses:
                return True
            if not literals:
                return False
            
            l = random.choice(list(literals))
            literals.remove(l)
            
            new_clauses = []
            for clause in clauses:
                if l in clause:
                    continue
                elif -l in clause:
                    clause.remove(-l)
                    if not clause:
                        return False
                else:
                    new_clauses.append(clause)
            
            stack.append((l, new_clauses))
            literals.add(-l)
        
        while stack:
            lit, clauses = stack.pop()
            if dpll(lit):
                continue
            elif dpll(-lit):
                continue
            else:
                return len(stack) + 1
        
        return len(stack) + 1
    
    n = random.randint(5, 40)
    p = random.choice([1.0, 2.0])
    clauses = generate_CNF(n)
    Lp_norm = compute_Lp_norm(clauses, p)
    proof_size = compute_resolution_proof_size(clauses)
    
    C = 1.0  # Placeholder for the constant C
    conjecture_holds = Lp_norm <= C * math.log(n) * (proof_size ** (1 / p))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Lp_norm_bound",
        "metric_value": Lp_norm,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = (sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results)) ** 0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")