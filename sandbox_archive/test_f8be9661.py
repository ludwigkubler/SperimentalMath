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

    def rank(A):
        A_rref = gaussian_elimination(A)
        r = 0
        for row in A_rref:
            if any(row):
                r += 1
        return r

    def is_k_sat_instance(G, k):
        # Placeholder function to check if G contains a k-SAT instance
        # This is a dummy implementation and should be replaced with actual logic
        return True

    def generate_dnf_circuits(G, k):
        # Placeholder function to generate all possible DNF circuits for k-SAT on G
        # This is a dummy implementation and should be replaced with actual logic
        return []

    n = random.randint(5, 40)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    if not is_k_sat_instance(G, k):
        return {
            "metric_name": "rank",
            "metric_value": rank(G),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "k-SAT instance not found"
        }

    dnf_circuits = generate_dnf_circuits(G, k)
    m_actual = min(len(circuit) for circuit in dnf_circuits)

    return {
        "metric_name": "rank",
        "metric_value": rank(G),
        "instances_tested": 1,
        "conjecture_holds": m_actual <= 2 ** rank(G),
        "counterexample": "" if m_actual <= 2 ** rank(G) else f"m_actual={m_actual} > 2^rank(G)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m_actual > 2^rank(G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")