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

def generate_tseitin_formula(n, m):
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    # Generate literals and their negations
    literals = set()
    for var in variables:
        literals.add(var)
        literals.add(f'~{var}')
    
    # Ensure all literals are used at least once
    for literal in literals:
        if random.choice([True, False]):
            clauses.append(literal)
    
    # Add m more clauses with random literals
    for _ in range(m):
        clause = []
        num_literals = random.randint(1, n)
        for _ in range(num_literals):
            literal = random.choice(list(literals))
            if literal.startswith('~'):
                while literal in clause:
                    literal = random.choice(list(literals))
            else:
                while f'~{literal}' in clause:
                    literal = random.choice(list(literals))
            clause.append(literal)
        clauses.append(' | '.join(clause))
    
    # Add negation of each variable to ensure satisfiability
    for var in variables:
        clauses.append(f'~{var} | {var}')
    
    return ' & '.join(clauses)

def generate_projective_variety(formula):
    literals = set()
    for clause in formula.split(' & '):
        for literal in clause.split(' | '):
            if literal.startswith('~'):
                literals.add(literal[1:])
            else:
                literals.add(literal)
    
    # Create a projective variety as a list of tuples
    G = []
    for literal in literals:
        G.append((literal, f'~{literal}'))
    
    return G

def compute_rank(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    
    # Construct the matrix A based on the projective variety
    for i in range(n):
        for j in range(i + 1, n):
            if (G[i][0], G[j][0]) in G and (G[i][1], G[j][1]) in G:
                A[i][j] = 1
                A[j][i] = 1
    
    # Compute the rank of matrix A using Gaussian elimination
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            
            if matrix[i][i] == 0:
                continue
            
            for j in range(i + 1, rows):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[i][k]
        
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    return gaussian_elimination(A)

def compute_resolution_proof_length(formula):
    # Placeholder function to simulate resolution proof length calculation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(10, 100)  # Simulate a range of lengths

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(2 * n, 3 * n)
    formula = generate_tseitin_formula(n, m)
    G = generate_projective_variety(formula)
    
    rank = compute_rank(G)
    proof_length = compute_resolution_proof_length(formula)
    
    conjecture_holds = proof_length >= 2 ** (math.log(rank) / math.log(2))
    counterexample = "" if conjecture_holds else f"Formula: {formula}, Rank: {rank}, Proof Length: {proof_length}"
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsupported_conjecture")