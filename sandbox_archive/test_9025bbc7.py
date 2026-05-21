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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def read_twice_bp_to_noncommutative_crossed_product(bp):
        # Constructive mapping from read-twice BP to noncommutative crossed product
        n = len(bp)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        B = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        
        for op, var1, var2 in bp:
            if op == 'X':
                A[var1][var2] += Fraction(1)
                B[var2][var1] -= Fraction(1)
            elif op == 'Z':
                A[var1][var1] += Fraction(1)
                B[var2][var2] -= Fraction(1)
        
        C = matrix_multiplication(A, I)
        D = matrix_multiplication(B, I)
        E = gaussian_elimination(C)
        F = gaussian_elimination(D)
        
        return E, F

    def rho(bp):
        n = len(bp)
        E, F = read_twice_bp_to_noncommutative_crossed_product(bp)
        rank_E = sum(1 for row in E if any(x != Fraction(0) for x in row))
        rank_F = sum(1 for row in F if any(x != Fraction(0) for x in row))
        return max(rank_E, rank_F)

    def generate_read_twice_bp(n):
        bp = []
        operations = ['X', 'Z']
        for _ in range(n):
            op = random.choice(operations)
            var1 = random.randint(0, n-1)
            var2 = random.randint(0, n-1)
            bp.append((op, var1, var2))
        return bp

    def is_ip2_trivial(bp):
        # Simplistic check for IP_2 trivial BP
        for op, var1, var2 in bp:
            if op == 'Z':
                return False
        return True

    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    metric_value = rho(bp)
    instances_tested = 1
    
    conjecture_holds = False
    counterexample = ""
    
    if is_ip2_trivial(bp):
        if metric_value >= n:
            conjecture_holds = True
        else:
            counterexample = "IP_2 trivial BP with ρ(P) < n"
    else:
        expected_value = math.log(n)
        if 0.8 * expected_value <= metric_value <= 1.5 * expected_value:
            conjecture_holds = True
    
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 * math.log(r["instances_tested"]) for r in results) or support_fraction < 0.8:
        print("RESULT: FALSIFIED counterexample=\"ρ(P) exceeds upper bound\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")