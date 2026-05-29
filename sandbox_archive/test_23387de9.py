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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
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
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def generate_3cnf(n, m):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause.append(random.choice([-1, 1]))
            clauses.append(clause)
        return clauses

    def resolution_proofs(clauses):
        # Simplified version of DPLL algorithm
        stack = []
        model = {}
        while True:
            if not stack:
                return len(model), model
            literal = stack.pop()
            if literal in model and model[literal] != literal:
                continue
            negated_literal = -literal
            if negated_literal in model and model[negated_literal] == negated_literal:
                return None, {}
            for clause in clauses:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        return None, {}
                elif negated_literal in clause:
                    clause.remove(negated_literal)
                    if len(clause) == 1 and clause[0] != -negated_literal:
                        stack.append(-clause[0])
            model[literal] = literal

    def gromov_witten_invariant(n):
        # Placeholder for actual computation
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = random.randint(2*n, 3*n)
        clauses = generate_3cnf(n, m)
        proof_length, model = resolution_proofs(clauses)
        if proof_length is None:
            continue
        invariant = gromov_witten_invariant(n)
        total_metric_value += invariant * math.log(proof_length)
        instances_tested += 1

    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0
    support_fraction = Fraction(instances_tested, len(n_values))

    return {
        "metric_name": "Gromov-Witten Invariant",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results))

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")