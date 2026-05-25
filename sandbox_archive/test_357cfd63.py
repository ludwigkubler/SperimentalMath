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

# Gaussian elimination to compute matrix rank
def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = max(range(rank, m), key=lambda i: abs(A[i][j]))
        if A[i_max][j] == 0:
            continue
        A[rank], A[i_max] = A[i_max], A[rank]
        for i in range(m):
            if i != rank:
                factor = A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

# Compute the quantum logarithm rank of a Tseitin clause set
def matrix_rank(A):
    return gaussian_elimination(A)

# Generate a random Tseitin clause set with n variables
def generate_tseitin_clause_set(n):
    clauses = []
    for i in range(1, n + 1):
        clauses.append([i])
        clauses.append([-i])
        for j in range(i + 1, n + 1):
            clauses.append([i, -j])
            clauses.append([-i, j])
            clauses.append([-i, -j])
    return clauses

# Generate a resolution proof for a Tseitin clause set
def generate_resolution_proof(clauses):
    proof = []
    while True:
        new_clause = None
        for i in range(len(proof)):
            for j in range(i + 1, len(proof)):
                if len(set(proof[i]) & set(proof[j])) == 2:
                    new_clause = [x for x in proof[i] if x not in proof[j]]
                    break
            if new_clause is not None:
                break
        if new_clause is None:
            return proof
        proof.append(new_clause)

# Run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30  # Number of variables in the Tseitin clause set
    clauses = generate_tseitin_clause_set(n)
    refutation_length = len(generate_resolution_proof(clauses))
    
    Q_C = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    rank_Q_C = matrix_rank(Q_C)
    
    metric_name = "Quantum Logarithm Rank"
    metric_value = rank_Q_C
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if refutation_length > 0:
        c = 2 ** (n / 4) * 2
        if rank_Q_C >= 2 ** (n / 4) and rank_Q_C <= 2 ** n / c:
            conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Main function to run multiple trials with different seeds
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Default list of 30 prime numbers
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        counterexample = "Q(C)={}, n={}, refutation_length={}".format(results[first_failing_seed]['metric_value'], 30, len(generate_resolution_proof(generate_tseitin_clause_set(30))))
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")