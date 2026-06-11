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

    def hodge_dimension(poly, p):
        n = len(poly)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if poly[i] != 0 and poly[j] != 0:
                    A[i][j] = Fraction(poly[i], poly[j])
                    A[j][i] = Fraction(poly[j], poly[i])
        rank = sum(1 for row in gaussian_elimination(A) if any(row))
        return rank

    def satisfiability_complexity(phi):
        n = len(phi)
        count = 0
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            if all(lit == (assignment[abs(lit)-1] ^ (lit < 0)) for lit in phi):
                count += 1
        return count

    n = random.randint(5, 40)
    p = random.choice([2, 3, 5, 7, 11])
    phi = [random.randint(-n, n) for _ in range(n)]
    
    poly = [1]
    for lit in phi:
        new_poly = [Fraction(0) for _ in range(len(poly) + abs(lit))]
        for i in range(len(poly)):
            if lit > 0:
                new_poly[i + lit] += poly[i]
            else:
                new_poly[-i - 1] -= poly[i]
        poly = new_poly
    
    hd = hodge_dimension(poly, p)
    sc = satisfiability_complexity(phi)
    
    return {
        "metric_name": "Hodge Dimension vs. Satisfiability Complexity",
        "metric_value": hd / sc,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if hd == sc else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_hd_sc_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_hd_sc_ratio} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")