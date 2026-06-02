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
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = find_pure_literal(cnf)
        if literal is None:
            literal = find_unit_clause(cnf)
            if literal is None:
                return False
        new_cnf = []
        for clause in cnf:
            if literal not in clause and -literal not in clause:
                new_cnf.append([l for l in clause if l != literal])
        return dpll(new_cnf, assignment | {literal: True}) or dpll(new_cnf, assignment | {-literal: False})
    
    def find_pure_literal(cnf):
        pure_literals = {}
        for clause in cnf:
            for literal in clause:
                if literal not in pure_literals:
                    pure_literals[literal] = 1
                else:
                    pure_literals[literal] -= 1
        return next((l for l, count in pure_literals.items() if count == -1), None)
    
    def find_unit_clause(cnf):
        for clause in cnf:
            if len(clause) == 1:
                return clause[0]
        return None
    
    def geometric_quantization_matrix(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for i in clause:
                for j in clause:
                    if i != j and abs(i) == abs(j):
                        Q[abs(i)][abs(j)] += 1
        return Q
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for col in range(n):
            pivot_row = -1
            for row in range(m):
                if matrix[row][col] != 0:
                    pivot_row = row
                    break
            if pivot_row == -1:
                continue
            rank += 1
            for r in range(m):
                if r != pivot_row:
                    factor = matrix[r][col] / matrix[pivot_row][col]
                    for c in range(n):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    proof_depths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        Q = geometric_quantization_matrix(cnf)
        r = matrix_rank(Q)
        d = len(cnf) if not dpll(cnf) else 1
        min_ranks.append(r)
        proof_depths.append(d)
    
    correlation_coefficient = (n_values[0] * sum(x*y for x, y in zip(min_ranks, proof_depths)) -
                               sum(min_ranks) * sum(proof_depths)) / math.sqrt(
                                   (n_values[0] * sum(x**2 for x in min_ranks) - sum(min_ranks)**2) *
                                   (n_values[0] * sum(y**2 for y in proof_depths) - sum(proof_depths)**2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.6 <= correlation_coefficient <= 0.8,
        "counterexample": "" if 0.6 <= correlation_coefficient <= 0.8 else "correlation_out_of_range"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if 0.6 <= res["metric_value"] <= 0.8) / len(results)
    
    if all(0.6 <= res["metric_value"] <= 0.8 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(res["counterexample"] == "correlation_out_of_range" for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["counterexample"] == "correlation_out_of_range")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")