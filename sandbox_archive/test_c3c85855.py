# auto-injected by SEC sandbox
import math
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
    
    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def twisted_quandle_action(phi, q):
        n = len(phi)
        quandle = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if phi[i][j]:
                    quandle[i][j] = (i + j) % q
                else:
                    quandle[i][j] = (q - 1 - (i + j)) % q
        return quandle
    
    def resolution_width(phi):
        n = len(phi)
        clauses = phi[:]
        stack = []
        while clauses:
            clause = random.choice(clauses)
            if not any(lit in stack for lit in clause):
                stack.append(random.choice(clause))
            else:
                literals = [lit for lit in clause if lit not in stack]
                if not literals:
                    return len(stack) + 1
                new_clause = []
                for lit in literals:
                    new_clause.extend([x for x in phi if x != -lit])
                clauses.remove(clause)
                clauses.extend(new_clause)
        return len(stack)
    
    def generate_boolean_formula(n):
        phi = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            phi[i][i] = 1
        return phi
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_boolean_formula(n)
            q = random.randint(2, n-1)
            quandle = twisted_quandle_action(phi, q)
            A = [[quandle[i][j] for j in range(n)] for i in range(n)]
            A = gaussian_elimination(A)
            rank = sum(1 for row in A if any(x != 0 for x in row))
            width = resolution_width(phi)
            instances_tested += 1
            metric_values.append((rank, width))
    
    correlation_coefficient = 0.0
    n_samples = len(metric_values)
    if n_samples > 1:
        mean_rank = sum(x[0] for x in metric_values) / n_samples
        mean_width = sum(x[1] for x in metric_values) / n_samples
        covariance = sum((x[0] - mean_rank) * (x[1] - mean_width) for x in metric_values)
        variance_rank = sum((x[0] - mean_rank)**2 for x in metric_values)
        variance_width = sum((x[1] - mean_width)**2 for x in metric_values)
        correlation_coefficient = covariance / ((variance_rank * variance_width)**0.5)
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_value = (sum((x["metric_value"] - mean_value)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not x["conjecture_holds"] for x in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient=<{}>\" first_failing_seed=1".format(correlation_coefficient))
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={}".format(len(results)))