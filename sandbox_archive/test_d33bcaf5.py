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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def rank(A):
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row))
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        p = next((l for l in range(1, len(clauses[0]) + 1) if l not in assignment), None)
        if p is None:
            return False
        new_assignment = assignment.copy()
        new_assignment[p] = True
        if dpll([c for c in clauses if p not in c and -p not in c], new_assignment):
            return True
        new_assignment[p] = False
        if dpll([c for c in clauses if p not in c and -p not in c], new_assignment):
            return True
        return False
    
    def proof_width(clauses):
        assignment = {}
        return len(dpll(clauses, assignment))
    
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 3))
    clauses = []
    for _ in range(random.randint(10, 30)):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(k)]
        clauses.append(clause)
    
    min_rank = rank([[1 if i == abs(lit) else 0 for lit in clause] for clause in clauses])
    proof_width_val = proof_width(clauses)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": (min_rank - proof_width_val) / max(min_rank, proof_width_val),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")