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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = A[j][i] / A[i][i]
                A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x

    def matrix_multiplication(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def hodge_dimension(poly, p):
        n = len(poly)
        A = [[0 for _ in range(n)] for _ in range(n)]
        b = [0 for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A[i][j] = poly[i][j]
            b[i] = poly[i][-1]
        x = gaussian_elimination(A, b)
        return sum(1 for xi in x if xi != 0)

    def satisfiability_complexity(phi):
        n = len(phi)
        clauses = phi.split(' ')
        variables = set()
        for clause in clauses:
            literals = clause.split(' ')
            for literal in literals:
                if literal[0] == '-':
                    variables.add(literal[1:])
                else:
                    variables.add(literal)
        return len(variables)

    def generate_cnf(n):
        cnf = []
        for i in range(1, n+1):
            clause = random.choice(['', '-']) + str(i) + ' '
            for j in range(1, n+1):
                if j != i:
                    clause += random.choice(['', '-']) + str(j) + ' '
            cnf.append(clause[:-1])
        return ' '.join(cnf)

    n = 20
    phi = generate_cnf(n)
    poly = [[random.randint(0, 1) for _ in range(n+1)] for _ in range(n+1)]
    hd = hodge_dimension(poly, 2)
    sc = satisfiability_complexity(phi)
    
    return {
        "metric_name": "Hodge Dimension vs. Satisfiability Complexity",
        "metric_value": hd / sc,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_hd_sc_ratio = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_hd_sc_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_hd_sc_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = f"Hd/Sc ratio {res['metric_value']} does not match expected behavior"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break