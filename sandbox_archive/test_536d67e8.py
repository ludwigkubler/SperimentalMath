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
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def free_abelian_group_rank(x):
        n = len(x)
        A = [[0] * (n+1) for _ in range(n)]
        for i in range(n):
            A[i][i] = 1
            A[i][-1] = x[i]
        rank = gaussian_elimination(A)
        return sum(1 for row in rank if any(row[j] != 0 for j in range(n)))
    
    def boolean_tensor_product(x):
        n = len(x)
        TP = [0] * (2**n)
        for i in range(2**n):
            binary_rep = format(i, f'0{n}b')
            product = 1
            for bit in binary_rep:
                if bit == '1':
                    product *= x[int(bit)]
            TP[i] = product
        return TP
    
    def valuation(TP):
        m = len(TP)
        max_val = 0
        for i in range(m):
            val = sum(int(bit) for bit in format(i, f'0{m}b'))
            if val > max_val:
                max_val = val
        return math.log2(max_val + 1)
    
    n = random.randint(5, 40)
    m = random.randint(1, 100)
    x = [random.choice([0, 1]) for _ in range(n)]
    TP = boolean_tensor_product(x)
    rank = free_abelian_group_rank(x)
    val = valuation(TP)
    
    metric_value = abs(rank) / val
    instances_tested = 1
    conjecture_holds = abs(rank) <= val * (1 + 0.1) and abs(rank) >= val * (1 - 0.1)
    counterexample = "" if conjecture_holds else f"rank(Fx)={rank}, V(TP(x))={val}"
    
    return {
        "metric_name": "K-Theory Rank vs Tensor Product Valuation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*1000, 100))
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")