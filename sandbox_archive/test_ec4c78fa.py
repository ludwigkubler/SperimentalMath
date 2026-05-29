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
    
    def generate_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_clause_satisfied(clause, assignment):
        for var in clause:
            if (var > 0 and assignment[var - 1]) or (var < 0 and not assignment[abs(var) - 1]):
                return True
        return False
    
    def find_shortest_resolution_proof_length(clauses):
        n = len(clauses)
        proof_length = [n] * (2 ** n)
        proof_length[0] = 0
        
        for i in range(1, 2 ** n):
            for j in range(n):
                if is_clause_satisfied(clauses[j], list(map(lambda x: bool(x & 1), bin(i)[2:].zfill(n)))):
                    new_assignment = list(map(lambda x: bool(x & 1), bin(i ^ (1 << j))[2:].zfill(n)))
                    proof_length[i] = min(proof_length[i], proof_length[sum(1 << k for k in range(n) if new_assignment[k])] + 1)
        
        return proof_length[-1]
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for i in range(cols):
            pivot_row = -1
            for j in range(rank, rows):
                if matrix[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row == -1:
                continue
            matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
            rank += 1
            for j in range(rows):
                if j != rank - 1 and matrix[j][i] != 0:
                    factor = Fraction(matrix[j][i], matrix[rank - 1][i])
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[rank - 1][k]
        return rank
    
    def compute_qcr(clauses, n):
        variables = list(range(1, n + 1))
        graded_ring = {0: [1]}
        for i in range(1, n + 1):
            new_elements = []
            for term in graded_ring[i - 1]:
                for var in variables:
                    if var not in term:
                        new_term = sorted(term + [var])
                        if new_term not in new_elements:
                            new_elements.append(new_term)
            graded_ring[i] = new_elements
        
        ideal = set()
        for clause in clauses:
            negated_clause = [-x for x in clause]
            for term in graded_ring[len(clause)]:
                if all(x in term for x in negated_clause):
                    ideal.add(tuple(term))
        
        qcr_matrix = []
        for i in range(len(graded_ring[n])):
            row = [0] * len(ideal)
            for j, element in enumerate(ideal):
                if any(var in element for var in graded_ring[n][i]):
                    row[j] = 1
            qcr_matrix.append(row)
        
        return gaussian_elimination(qcr_matrix)
    
    n = random.randint(5, 40)
    k = random.randint(n // 2, n)
    clauses = generate_kcnf(n, k)
    
    qcr = compute_qcr(clauses, n)
    l_F = find_shortest_resolution_proof_length(clauses)
    
    return {
        "metric_name": "qcr(R_F)",
        "metric_value": qcr,
        "instances_tested": 1,
        "conjecture_holds": qcr == l_F,
        "counterexample": "" if qcr == l_F else f"qcr(R_F)={qcr}, l(F)={l_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results))
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif counterexample:
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'])), 0]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")