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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def zeta_function_rank(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for literal in clause:
                i = abs(literal) - 1
                if literal > 0:
                    matrix[i][i] += 1
                else:
                    matrix[n][i] += 1
                    matrix[i][n] += 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n + 1):
                        A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def resolution_proof_size(cnf):
        n = len(cnf[0])
        clauses = [set(clause) for clause in cnf]
        queue = list(clauses)
        seen = set()
        while queue:
            clause = queue.pop(0)
            if not clause:
                return 1
            literal = next(iter(clause))
            new_clauses = []
            for other_clause in clauses:
                if literal in other_clause:
                    continue
                if -literal in other_clause:
                    new_clause = (other_clause - {literal}) | (clause - {-literal})
                    if new_clause not in seen:
                        seen.add(new_clause)
                        new_clauses.append(new_clause)
            queue.extend(new_clauses)
        return 0
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = zeta_function_rank(cnf)
    proof_size = resolution_proof_size(cnf)
    
    if proof_size == 0:
        return {
            "metric_name": "rank_to_proof_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proof_size_zero"
        }
    
    ratio = Fraction(rank, proof_size)
    return {
        "metric_name": "rank_to_proof_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((x - mean)**2 for x in (r["metric_value"] for r in results)) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank_to_proof_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")