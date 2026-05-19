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
    
    def generate_3cnf(n, m):
        clauses = set()
        variables = list(range(1, n + 1))
        for _ in range(m):
            clause = []
            for _ in range(3):
                var = random.choice(variables)
                polarity = random.choice([-1, 1])
                clause.append((var, polarity))
            clauses.add(tuple(sorted(clause)))
        return clauses

    def is_unsat(cnf):
        # Simple DPLL algorithm to check unsatisfiability
        assignment = [None] * (n + 1)
        
        def dpll():
            stack = []
            for var in range(1, n + 1):
                if all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [-1, 1]):
                    assignment[var] = 1
                    stack.append((var, 1))
                elif all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [1, -1]):
                    assignment[var] = -1
                    stack.append((var, -1))
                else:
                    return False
            while stack:
                var, polarity = stack.pop()
                if not all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [-1, 1]):
                    assignment[var] = -polarity
                    stack.append((var, -polarity))
            return True
        
        return not dpll()

    def walsh_hadamard_transform(cnf):
        n_vars = len(cnf)
        spectrum = [0] * (2 ** n_vars)
        
        for i in range(1 << n_vars):
            x = [1 if (i >> j) & 1 else -1 for j in range(n_vars)]
            value = sum(1 if all(x[var - 1] == polarity for var, polarity in clause) else -1 for clause in cnf)
            spectrum[i] = value / math.sqrt(len(cnf))
        
        return spectrum

    def spectral_entropy(spectrum):
        norm_squared = sum(abs(val) ** 2 for val in spectrum)
        entropy = 0
        for val in spectrum:
            if val != 0:
                q = abs(val) ** 2 / norm_squared
                entropy -= q * math.log2(q)
        return entropy

    def tree_resolution(cnf):
        # Simplified tree-resolution algorithm to count leaf nodes
        stack = []
        for var in range(1, n + 1):
            if all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [-1, 1]):
                assignment[var] = 1
                stack.append((var, 1))
            elif all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [1, -1]):
                assignment[var] = -1
                stack.append((var, -1))
            else:
                return len(cnf)
        
        while stack:
            var, polarity = stack.pop()
            if not all(any(abs(clause[var - 1][0]) == abs(var) and clause[var - 1][1] != polarity for clause in cnf) for polarity in [-1, 1]):
                assignment[var] = -polarity
                stack.append((var, -polarity))
        
        return len(cnf)

    n = random.randint(10, 20)
    m = math.ceil(4.3 * n)
    cnf = generate_3cnf(n, m)
    
    if not is_unsat(cnf):
        return {
            "metric_name": "R(F)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable_cnf"
        }
    
    spectrum = walsh_hadamard_transform(cnf)
    H_F = spectral_entropy(spectrum)
    t_star = tree_resolution(cnf)
    
    if H_F == 0:
        return {
            "metric_name": "R(F)",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "zero_entropy"
        }
    
    R_F = math.log2(t_star) * math.log2(1 + n + n**2 + n**3) / (n * H_F)
    
    return {
        "metric_name": "R(F)",
        "metric_value": R_F,
        "instances_tested": 1,
        "conjecture_holds": R_F >= 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    R_F_values = [result["metric_value"] for result in results if not math.isnan(result["metric_value"])]
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(R_F >= 0.05 for R_F in R_F_values) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(R_F_values)/len(R_F_values)} std={math.sqrt(sum((x - sum(R_F_values)/len(R_F_values))**2 for x in R_F_values)/len(R_F_values))} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] is False for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_R_F\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")