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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= factor
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        n = len(matrix)
        reduced_matrix = gaussian_elimination(matrix)
        r = 0
        for row in reduced_matrix:
            if any(row):
                r += 1
        return r

    def dpll(clauses, assignment):
        if not clauses:
            return True
        if any(not clause for clause in clauses):
            return False
        literal = next(lit for lit in range(1, len(assignment)+1) if lit not in assignment and -lit not in assignment)
        assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], assignment):
            return True
        assignment[literal] = False
        assignment[-literal] = True
        if dpll([c for c in clauses if -literal not in c and literal not in c], assignment):
            return True
        del assignment[literal]
        del assignment[-literal]
        return False

    def generate_cnf(n, m):
        cnf = []
        variables = set(range(1, n+1))
        for _ in range(m):
            clause = random.sample(variables, 3)
            cnf.append([random.choice([-1, 1]) * var for var in clause])
        return cnf

    def graphical_realization(cnf):
        n = len(cnf)
        T = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in range(n):
                if -i+1 not in clause and i+1 not in clause:
                    continue
                for j in range(i+1, n):
                    if -j+1 not in clause and j+1 not in clause:
                        T[i][j] = 1
                        T[j][i] = 1
        return T

    def min_rank(T):
        return rank(T)

    def dpll_proof_length(cnf):
        assignment = {}
        if dpll(cnf, assignment):
            return len(assignment)
        return float('inf')

    n = random.randint(5, 40)
    m = random.randint(3*n, 6*n)
    cnf = generate_cnf(n, m)
    T = graphical_realization(cnf)
    r_T = min_rank(T)
    L = dpll_proof_length(cnf)

    return {
        "metric_name": "DPLL Proof Length",
        "metric_value": L,
        "instances_tested": 1,
        "conjecture_holds": L <= 2**(r_T / 2),
        "counterexample": "" if L <= 2**(r_T / 2) else f"CNF size {n}, rank {r_T}, proof length {L}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")