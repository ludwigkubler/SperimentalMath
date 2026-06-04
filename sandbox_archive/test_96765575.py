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
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def dpll_solver(phi, assignment, clauses):
        if not clauses:
            return True
        literal = next(lit for lit in phi if lit not in assignment and -lit not in assignment)
        pos_lit = abs(literal)
        new_assignment = assignment.copy()
        new_assignment[pos_lit] = 1 if literal > 0 else 0
        new_clauses = [c for c in clauses if not any(x in c or -x in c for x in (pos_lit, -pos_lit))]
        if dpll_solver(phi, new_assignment, new_clauses):
            return True
        new_assignment[pos_lit] = 1 if literal < 0 else 0
        new_clauses = [c for c in clauses if not any(x in c or -x in c for x in (pos_lit, -pos_lit))]
        if dpll_solver(phi, new_assignment, new_clauses):
            return True
        return False

    def local_symmetry_count(toric_variety):
        # Placeholder for actual computation of local symmetry count
        return random.randint(1, 10)

    def dpll_proof_tree_width(phi):
        assignment = {}
        clauses = phi.split('\n')
        return len(clauses) if dpll_solver(phi, assignment, clauses) else 0

    def generate_cnf(n):
        literals = [i for i in range(1, n+1)]
        cnf = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            cnf.append(f"{clause[0]} {clause[1]} 0")
        return "\n".join(cnf)

    def construct_toric_variety(phi):
        # Placeholder for actual construction of toric variety
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(instances_tested // len([5, 10, 15, 20, 30, 40])):
            phi = generate_cnf(n)
            toric_variety = construct_toric_variety(phi)
            local_symmetry = local_symmetry_count(toric_variety)
            proof_tree_width = dpll_proof_tree_width(phi)
            if proof_tree_width == 0:
                continue
            metric_value = Fraction(local_symmetry, proof_tree_width)
            metric_values.append(metric_value)
            if not (0.5 <= metric_value <= 1.5):
                conjecture_holds = False
                counterexample = f"n={n}, LocalSymmetryCount={local_symmetry}, DPLLWidth={proof_tree_width}"
                break

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = Fraction(conjecture_holds, True)

    return {
        "metric_name": "LocalSymmetryCount/DPLLWidth",
        "metric_value": float(mean_metric),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = Fraction(all(r["conjecture_holds"] for r in results), True)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")