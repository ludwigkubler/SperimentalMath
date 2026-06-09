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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment:
                return False
            elif literal > 0 and literal not in assignment:
                assignment[literal] = True
                return dpll([c for c in clauses if literal not in c], assignment)
            else:
                assignment[-literal] = False
                return dpll([c for c in clauses if -literal not in c], assignment)
        pure_literal = next((l for l in range(1, len(clauses)+1) if all(l in c or -l in c for c in clauses)), None)
        if pure_literal:
            literal = pure_literal
            if literal < 0 and -literal in assignment:
                return False
            elif literal > 0 and literal not in assignment:
                assignment[literal] = True
                return dpll(clauses, assignment)
            else:
                assignment[-literal] = False
                return dpll(clauses, assignment)
        var = next((i for i in range(1, len(clauses)+1) if i not in assignment and -i not in assignment), None)
        if var is None:
            return True
        assignment[var] = True
        if dpll([c for c in clauses if var not in c], assignment):
            return True
        assignment[var] = False
        assignment[-var] = True
        if dpll([c for c in clauses if -var not in c], assignment):
            return True
        return False

    def frege_proof_depth(clauses):
        assignment = {}
        return len(dpll(clauses, assignment)) + 1

    def construct_metric_space(clauses):
        n = len(clauses)
        M = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(l in clauses[i] and -l in clauses[j] for l in range(1, 2*n)):
                    M[i][j] = 1
                else:
                    M[i][j] = 0
        return M

    def minimal_geometric_entropy(M):
        n = len(M)
        I = [[Fraction(1, n)]*n for _ in range(n)]
        A = gaussian_elimination(matrix_multiply(I, M))
        det = 1
        for i in range(n):
            det *= A[i][i]
        return -math.log2(det)

    def generate_cnf(n):
        clauses = []
        for _ in range(2*n):
            clause = random.sample(range(1, n+1), 3)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    n_max = 40
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max+1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            clauses = generate_cnf(n)
            M = construct_metric_space(clauses)
            het_M = minimal_geometric_entropy(M)
            d_phi = frege_proof_depth(clauses)
            metric_values.append((het_M, d_phi))
            instances_tested += 1

    if len(metric_values) < 30:
        return {
            "metric_name": "Frege proof depth vs. geometric entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }

    het_values, d_phi_values = zip(*metric_values)
    correlation_coefficient = sum((het - mean(het_values)) * (d - mean(d_phi_values)) for het, d in metric_values) / math.sqrt(sum((het - mean(het_values))**2 for het in het_values) * sum((d - mean(d_phi_values))**2 for d in d_phi_values))

    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"

    return {
        "metric_name": "Frege proof depth vs. geometric entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    for result in results:
        print(f"TRIAL: {result}")

    mean_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] or r["counterexample"] == "not_enough_instances" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False and r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")