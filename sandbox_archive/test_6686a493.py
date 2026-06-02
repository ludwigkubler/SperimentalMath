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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
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

    def alexander_module_order(G):
        n = len(G)
        if n == 0:
            return 0
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(n):
            A[i][i] = 1
            for j in G[i]:
                A[i][j] = -1
                A[j][i] = -1
        A[-1][-1] = 1
        rank = 0
        for i in range(n+1):
            if determinant(gaussian_elimination(A[:i+1])) != 0:
                rank += 1
        return rank

    def generate_random_protocol(n, k):
        participants = list(range(n))
        protocol = []
        while len(protocol) < k:
            sender, receiver = random.sample(participants, 2)
            if (sender, receiver) not in protocol and (receiver, sender) not in protocol:
                protocol.append((sender, receiver))
        return protocol

    def interaction_graph(protocol):
        n = max(max(p) for p in protocol) + 1
        G = [[] for _ in range(n)]
        for s, r in protocol:
            G[s].append(r)
            G[r].append(s)
        return G

    n_values = [5, 10, 15, 20, 30, 40]
    total_order = 0
    instances_tested = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            protocol = generate_random_protocol(n, k)
            G = interaction_graph(protocol)
            order = alexander_module_order(G)
            total_order += order
            instances_tested += 1
            max_n = max(max_n, n)
            if order > 2 * math.log(n / k):
                conjecture_holds = False
                counterexample = f"n={n}, protocol={protocol}, order={order}"

    mean_order = total_order / instances_tested
    support_fraction = (mean_order <= 1.5 * math.log(n / k)) and not conjecture_holds

    return {
        "metric_name": "Alexander Module Order",
        "metric_value": mean_order,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": support_fraction,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")