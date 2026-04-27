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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [M[i][-1] for i in range(n)]

def hessian_rank(p_F, n):
    H_F = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for x in range(3**n):
        x_vec = [(x // (3 ** i)) % 3 for i in range(n)]
        for i in range(n):
            for j in range(i, n):
                H_F[i][j] += p_F[x_vec] * (-1)**(x_vec[i] + x_vec[j])
                if i != j:
                    H_F[j][i] = H_F[i][j]
    rank = 0
    for row in H_F:
        if any(row):
            rank += 1
    return rank

def lex_dpll(F, n):
    def dpll(assignment):
        unsatisfied_clauses = [C for C in F if not any(l == assignment[i] for i, l in enumerate(C))]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((C for C in unsatisfied_clauses if len(C) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
                assignment[literal-1] = 0
            else:
                assignment[literal-1] = 1
            return dpll(assignment)
        for literal in range(1, n+1):
            if literal not in [abs(l) for l in assignment]:
                new_assignment = assignment[:]
                new_assignment.append(literal)
                if dpll(new_assignment):
                    return True
                if -literal not in [abs(l) for l in assignment]:
                    new_assignment = assignment[:]
                    new_assignment.append(-literal)
                    if dpll(new_assignment):
                        return True
        return False
    return dpll([0]*n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 7, 8, 9, 10, 11]
    alpha = 5.0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        num_instances = 40 if n <= 7 else 300
        for _ in range(num_instances):
            F = []
            while len(F) < alpha * n / 100:
                C = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(3)]
                if all(l not in C or l != -l2 for l, l2 in zip(C, F)):
                    F.append(C)
            p_F = [0] * (3**n)
            for x in range(3**n):
                x_vec = [(x // (3 ** i)) % 3 for i in range(n)]
                product = Fraction(1)
                for l in F:
                    if l > 0 and x_vec[l-1] == 2:
                        product *= 0
                    elif l < 0 and x_vec[-l-1] == 0:
                        product *= 0
                    else:
                        product *= (x_vec[abs(l)-1] if l > 0 else 1 - x_vec[-l-1])
                p_F[x] = product
            
            r_F = hessian_rank(p_F, n)
            d_DPLL_F = lex_dpll(F, n)
            
            instances_tested += 1
            if r_F < d_DPLL_F:
                conjecture_holds = False
                counterexample = f"n={n}, r(F)={r_F}, d_DPLL(F)={d_DPLL_F}"
    
    return {
        "metric_name": "Hessian-Rank",
        "metric_value": instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")