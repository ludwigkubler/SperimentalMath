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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = Fraction(matrix[i][i])
            for j in range(i, n + 1):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = Fraction(matrix[j][i])
                    for k in range(i, n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def determinant(matrix):
        n = len(matrix)
        det = Fraction(1)
        for i in range(n):
            det *= matrix[i][i]
        return det

    def tropical_hodge_norm(matrix):
        n = len(matrix)
        max_val = -math.inf
        for row in matrix:
            for val in row:
                if val > max_val:
                    max_val = val
        return max_val

    def resolution_proof_length(cnf):
        # Simplified DPLL solver to estimate proof length
        stack = []
        assignment = {}
        def dpll():
            if not cnf:
                return True, 1
            literal = next((l for l in range(1, len(cnf) + 1) if l not in assignment and -l not in assignment), None)
            if literal is None:
                return False, 0
            assignment[literal] = True
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                if -literal in clause:
                    clause.remove(-literal)
                if len(clause) == 0:
                    return False, 0
                new_cnf.append(clause)
            result, length = dpll()
            if result:
                return True, length + 1
            del assignment[literal]
            assignment[-literal] = True
            for clause in cnf:
                if -literal in clause:
                    continue
                if literal in clause:
                    clause.remove(literal)
                if len(clause) == 0:
                    return False, 0
                new_cnf.append(clause)
            result, length = dpll()
            if result:
                return True, length + 1
            del assignment[-literal]
            return False, 0
        return dpll()[1]

    def generate_random_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = random.sample(range(1, n+1), random.randint(1, n))
            cnf.append(clause)
        return cnf

    n = 30
    instances_tested = 0
    support_count = 0
    counterexample = ""

    for _ in range(30):
        cnf = generate_random_cnf(n)
        matrix = [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        hodge_norm = tropical_hodge_norm(matrix)
        proof_length = resolution_proof_length(cnf)
        if proof_length > 0:
            instances_tested += 1
            ratio = Fraction(hodge_norm, math.log(n))
            if ratio >= 2**proof_length / math.log(n):
                support_count += 1
            else:
                counterexample = f"CNF with n={n} requires less than 2^k / log(n) resolution steps"

    return {
        "metric_name": "Resolution Proof Length Ratio",
        "metric_value": support_count / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": support_count / instances_tested >= 0.8 if instances_tested > 0 else False,
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

    support_count = sum(r["support_count"] for r in results if "support_count" in r and r["instances_tested"] > 0)
    instances_tested = sum(r["instances_tested"] for r in results if "instances_tested" in r)
    support_fraction = support_count / instances_tested if instances_tested > 0 else 0

    if all("support_count" in r and r["instances_tested"] > 0 and r["support_count"] >= 0.8 * r["instances_tested"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any("support_count" in r and r["instances_tested"] > 0 and r["support_count"] < 0.8 * r["instances_tested"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "support_count" in r and r["instances_tested"] > 0 and r["support_count"] < 0.8 * r["instances_tested"])
        print(f"RESULT: FALSIFIED counterexample=\"CNF with n=30 requires less than 2^k / log(n) resolution steps\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")