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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def rank(A):
        A = gaussian_elimination(A)
        r = 0
        for row in A:
            if any(row):
                r += 1
        return r

    def monotone_circuit_depth(n):
        # Simplified model of monotone circuit depth for k-CLIQUE
        return math.ceil(math.log2(n))

    n = random.choice([5, 10, 15, 20, 30, 40])
    A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    rank_A = rank(A)
    rank_B = rank(B)

    depth_A = monotone_circuit_depth(n)
    depth_B = monotone_circuit_depth(n)

    if rank_A == 0 or rank_B == 0:
        return {
            "metric_name": "monotone_circuit_depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    c = depth_A / rank_A
    if depth_B > c * rank_B:
        return {
            "metric_name": "monotone_circuit_depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: depth_A={depth_A}, rank_A={rank_A}, depth_B={depth_B}, rank_B={rank_B}"
        }

    return {
        "metric_name": "monotone_circuit_depth",
        "metric_value": c,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_c = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_c = math.sqrt(sum((r["metric_value"] - mean_c)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_c} std={std_c} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")