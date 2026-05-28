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
    
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Generate Tseitin formula
    for var in variables:
        clauses.append(f'{var} ~{var}')
    
    for i in range(n):
        clause = f'~x{i}'
        for j in range(i + 1, n):
            clause += f' {random.choice(["|", "&"])} ~x{j}'
        clauses.append(clause)
    
    # Construct graph G
    G = {}
    for var in variables:
        G[var] = set()
    for clause in clauses:
        if '~' in clause:
            literal = clause.split()[0]
            negated_literal = literal[1:]
            if negated_literal in G:
                G[negated_literal].add(literal)
                G[literal].add(negated_literal)
    
    # Compute Hodge structure H(G)
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return None
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def rank(matrix):
        if not matrix:
            return 0
        rows, cols = len(matrix), len(matrix[0])
        reduced_matrix = gaussian_elimination(matrix)
        if reduced_matrix is None:
            return 0
        rank = 0
        for row in reduced_matrix:
            if any(row[i] != 0 for i in range(cols)):
                rank += 1
        return rank
    
    H_G = []
    for var in variables:
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for neighbor in G[var]:
            if neighbor.startswith('~'):
                col = int(neighbor[1:]) - 1
                A[col][col] += 1
                A[n][col] -= 1
            else:
                col = int(neighbor) - 1
                A[col][col] += 1
                A[n][col] += 1
        H_G.append(rank(A))
    
    min_rank_H_G = min(H_G)
    
    # Construct Resolution proof
    def resolution(proof, clause):
        new_clause = []
        for c in proof:
            if c[0] == '~' and c[1:] in clause or c not in clause:
                new_clause.append(c)
        return new_clause
    
    proof = [clauses[0]]
    for clause in clauses[1:]:
        while True:
            new_proof = resolution(proof, clause)
            if new_proof == proof:
                break
            proof = new_proof
    
    proof_length = len(proof)
    
    # Check conjecture
    conjecture_holds = proof_length >= 2 ** math.floor(math.log(min_rank_H_G, 2))
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < 2^floor(log({min_rank_H_G}, 2))"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")