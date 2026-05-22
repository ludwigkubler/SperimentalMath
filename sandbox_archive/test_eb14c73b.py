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
    
    def generate_cnf(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [-v for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def gram_matrix(cnf):
        n = len(cnf)
        M = [[0] * n for _ in range(n)]
        for i, clause in enumerate(cnf):
            for j, clause2 in enumerate(cnf):
                count = sum(1 for v in clause if -v in clause2)
                M[i][j] = count
        return M
    
    def smith_normal_form(M):
        n = len(M)
        U = [[0] * n for _ in range(n)]
        V = [[0] * n for _ in range(n)]
        for i in range(n):
            U[i][i] = 1
            V[i][i] = 1
        
        def pivot(M, r, c):
            M[r], M[c] = M[c], M[r]
            for j in range(c+1, n):
                M[r][j] /= M[r][c]
            for i in range(n):
                if i != r:
                    factor = M[i][c]
                    for j in range(c, n):
                        M[i][j] -= factor * M[r][j]
        
        def find_pivot(M):
            for i in range(n):
                for j in range(n):
                    if M[i][j] != 0:
                        return i, j
            return None
        
        while True:
            pivot_row, pivot_col = find_pivot(M)
            if pivot_row is None:
                break
            pivot(M, pivot_row, pivot_col)
        
        for r in range(n):
            for c in range(r+1, n):
                M[r][c] = 0
        
        return M
    
    def resolution_length(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i+1, len(stack)):
                    clause_i = set(stack[i])
                    clause_j = set(stack[j])
                    if any(-v in clause_i for v in clause_j):
                        new_clause = [v for v in clause_i | clause_j if v not in [-v for v in clause_i] and v not in [-v for v in clause_j]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    gram = gram_matrix(cnf)
    snf = smith_normal_form(gram)
    rank = sum(1 for row in snf if any(x != 0 for x in row))
    
    proof_length = resolution_length(cnf)
    
    return {
        "metric_name": "Ratio of Rank to Proof Length",
        "metric_value": rank / proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank <= 10 ** (1/2) * proof_length,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 100000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > sqrt(proof_length)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget exceeded")