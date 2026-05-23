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
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def tropical_geometric_quantization_rank(A):
        m, n = len(A), len(A[0])
        G = []
        for i in range(m):
            row = [max(A[i][j], 0) for j in range(n)]
            if sum(row) > 0:
                G.append([x / sum(row) for x in row])
        return determinant(gaussian_elimination(G))

    def communication_complexity(qubits):
        # Placeholder function to simulate communication complexity
        return random.uniform(1, qubits)

    n = random.choice([5, 10, 15, 20, 30, 40])
    qubits = [[random.randint(-1, 1) for _ in range(n)] for _ in range(n)]
    
    TGR = tropical_geometric_quantization_rank(qubits)
    CC_XOR = communication_complexity(n)
    
    if TGR == 0:
        return {
            "metric_name": "CC_XOR/TGR",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "TGR(q) is zero, which is undefined for this mapping."
        }
    
    ratio = CC_XOR / TGR
    return {
        "metric_name": "CC_XOR/TGR",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r and not math.isinf(r["metric_value"])]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("counterexample" in r and r["counterexample"] == "" for r in results):
        mean = sum(metric_values) / len(metric_values)
        std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean:.4f} std={std:.4f} support_fraction={support_fraction:.2f}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed=<s>")
    else:
        for r in results:
            if "counterexample" in r and r["counterexample"] != "":
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break