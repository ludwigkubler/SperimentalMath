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
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        det = Fraction(1)
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            det *= A[i][i]
            for j in range(i+1, m):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return det
    
    def rank(A):
        m, n = len(A), len(A[0])
        A_rref = gaussian_elimination(A)
        r = 0
        for i in range(m):
            if any(A_rref[i][j] != Fraction(0) for j in range(n)):
                r += 1
        return r
    
    def tseitin_formula(variables, clauses):
        n = len(variables)
        literals = [f"x{i}" for i in range(n)]
        negated_literals = [f"¬x{i}" for i in range(n)]
        formulas = []
        for literal in literals:
            formulas.append(literal)
        for clause in clauses:
            formula = "∨".join(clause)
            formulas.append(f"(¬{formula})")
        return formulas
    
    def dpll(formulas, assignment):
        if not formulas:
            return True
        formula = formulas[0]
        if formula.startswith("¬"):
            literal = formula[2:]
            if literal in assignment and assignment[literal] == "true":
                return False
            elif literal not in assignment:
                assignment[literal] = "false"
                if dpll(formulas, assignment):
                    return True
                del assignment[literal]
                assignment[literal] = "true"
                if dpll(formulas, assignment):
                    return True
                del assignment[literal]
        else:
            literal = formula
            if literal in assignment and assignment[literal] == "false":
                return False
            elif literal not in assignment:
                assignment[literal] = "true"
                if dpll(formulas, assignment):
                    return True
                del assignment[literal]
                assignment[literal] = "false"
                if dpll(formulas, assignment):
                    return True
                del assignment[literal]
        return False
    
    def count_steps_to_refutation(variables, clauses):
        formulas = tseitin_formula(variables, clauses)
        assignment = {}
        steps = 0
        while not dpll(formulas, assignment):
            literal = random.choice(list(assignment.keys()))
            if assignment[literal] == "true":
                del assignment[literal]
            else:
                assignment[literal] = "false"
            steps += 1
        return steps
    
    n = random.randint(5, 40)
    variables = [f"x{i}" for i in range(n)]
    clauses = []
    for _ in range(random.randint(2, n)):
        clause = random.sample(variables + negated_literals, random.randint(1, n))
        clauses.append(clause)
    
    curve = sum(coeff * x**i for i, coeff in enumerate([random.randint(-10, 10) for _ in range(n+1)])) if n > 0 else 0
    rank_T = rank([[coeff] for coeff in [random.randint(-10, 10) for _ in range(n+1)]]) if n > 0 else 0
    
    steps_to_refutation = count_steps_to_refutation(variables, clauses)
    
    return {
        "metric_name": "steps_to_refutation",
        "metric_value": steps_to_refutation,
        "instances_tested": 1,
        "conjecture_holds": steps_to_refutation >= 2**rank_T,
        "counterexample": "" if steps_to_refutation >= 2**rank_T else f"Rank {rank_T}, Steps {steps_to_refutation}"
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank {results[0]['counterexample']}\", first_failing_seed={first_failing_seed}")