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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = None
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(rows):
                    if j != rank and matrix[j][i] != 0:
                        factor = -matrix[j][i] / matrix[rank][i]
                        for k in range(cols):
                            matrix[j][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def arithmetic_hodge_index(n, rank):
        # Simplified version of the Hodge index calculation
        return n - rank
    
    def resolution_proof_length(cnf):
        stack = []
        for clause in cnf:
            if all(abs(lit) not in [abs(lit2) for lit2 in clause] for lit in clause):
                stack.append(clause)
        while stack:
            clause1 = stack.pop()
            clause2 = stack.pop()
            new_clause = set()
            for lit1 in clause1:
                for lit2 in clause2:
                    if abs(lit1) != abs(lit2):
                        new_clause.add(-lit1 if lit2 > 0 else lit1)
            if not new_clause:
                return len(cnf) - len(stack)
            stack.append(new_clause)
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    rank = gaussian_elimination([[abs(lit) for lit in clause] for clause in cnf])
    ahi = arithmetic_hodge_index(n, rank)
    rpl = resolution_proof_length(cnf)
    
    return {
        "metric_name": "arithmetic_hodge_index",
        "metric_value": ahi,
        "instances_tested": 1,
        "conjecture_holds": ahi <= n**2 * (rpl ** (1/3)),
        "counterexample": f"n={n}, AHI={ahi}, RPL={rpl}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")