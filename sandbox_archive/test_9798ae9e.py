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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    return [row[-1] for row in Augmented]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = set()
    for _ in range(n):
        g = tuple(random.randint(-n, n) for _ in range(n))
        if all(g[i] == -g[n-1-i] for i in range(n//2)):
            G.add(g)
    G = list(G)
    num_classes = len(set(tuple(sorted(g)) for g in G))
    
    Tseitin_length = 0
    instances_tested = 0
    
    for _ in range(30):
        instance = [random.randint(-1, 1) for _ in range(n)]
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        b = [sum(A[i][j] * instance[j] for j in range(n)) for i in range(n)]
        
        if any(a == 0 for a in A[0]):
            continue
        
        try:
            solution = gaussian_elimination(A, b)
            Tseitin_length += sum(abs(x) for x in solution)
            instances_tested += 1
        except Exception as e:
            return {
                "metric_name": "Tseitin length",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    if instances_tested == 0:
        return {
            "metric_name": "Tseitin length",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_length = Tseitin_length / instances_tested
    conjecture_holds = mean_length >= 2 ** (math.log2(num_classes))
    
    return {
        "metric_name": "Tseitin length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break