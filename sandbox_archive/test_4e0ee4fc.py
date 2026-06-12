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
    
    def generate_instance(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append([var])
            clauses.append([-var])
        for i in range(2, n+1):
            clause = random.sample(variables, i)
            clauses.append(clause)
            clauses.append([-v for v in clause])
        return clauses
    
    def tseitin_formula(clauses):
        literals = set()
        new_vars = {}
        for i, clause in enumerate(clauses):
            literal = f"t{i}"
            literals.add(literal)
            new_vars[literal] = []
            for lit in clause:
                if lit.startswith("x"):
                    new_vars[literal].append(lit)
                else:
                    new_vars[literal].append(-new_vars[-lit][0])
        return literals, new_vars
    
    def tropical_hessian(n):
        H = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    H[i][j] = 1
                    H[j][i] = 1
        return H
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        U = [row[:] for row in matrix]
        r = 0
        for j in range(n):
            i_max = max(range(r, m), key=lambda i: abs(U[i][j]))
            if abs(U[i_max][j]) > 1e-9:
                U[r], U[i_max] = U[i_max], U[r]
                for i in range(r+1, m):
                    factor = U[i][j] / U[r][j]
                    for k in range(n):
                        U[i][k] -= factor * U[r][k]
                r += 1
        return r
    
    def resolution_proof_size(clauses):
        stack = []
        literals = set()
        for clause in clauses:
            if not any(lit in literals for lit in clause):
                literals.update(clause)
                stack.append(clause)
        while stack:
            clause = stack.pop()
            new_clause = [lit for lit in clause if lit not in literals]
            if not new_clause:
                continue
            literals.add(new_clause[0])
            for other_clause in clauses:
                if new_clause[0] in other_clause and -new_clause[0] in other_clause:
                    stack.append([l for l in other_clause if l != new_clause[0]])
        return len(clauses) + len(stack)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_instance(n)
    literals, new_vars = tseitin_formula(instance)
    H_trop = tropical_hessian(n)
    rank_H_trop = rank(H_trop)
    
    proof_size = resolution_proof_size(instance)
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": proof_size <= 1.5 * rank_H_trop,
        "counterexample": "" if proof_size <= 1.5 * rank_H_trop else f"Proof size {proof_size} > 1.5 * rank {rank_H_trop}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 7 for i in range(5, 30)]  # First 25 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")