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
            # Find pivot
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below pivot
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back-substitute to get the solution
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = A[i][-1] / A[i][i]
            for j in range(i):
                A[j][-1] -= A[j][i] * x[i]
        return x
    
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
            return 1
        
        # Construct the adjacency matrix
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j]:
                    A[i][j], A[j][i] = 1, 1
        
        # Compute the determinant of the adjacency matrix
        det_A = determinant(A)
        
        # The order of the Alexander module is the absolute value of the determinant
        return abs(det_A)
    
    def generate_k_communication_protocol(n, k):
        participants = list(range(n))
        protocol = []
        for _ in range(k):
            sender, receiver = random.sample(participants, 2)
            protocol.append((sender, receiver))
        return protocol
    
    def interaction_graph(protocol, n):
        G = [[0] * n for _ in range(n)]
        for s, r in protocol:
            G[s][r], G[r][s] = 1, 1
        return G
    
    n = random.randint(5, 40)
    k = random.randint(1, min(n-1, 3))
    protocol = generate_k_communication_protocol(n, k)
    G = interaction_graph(protocol, n)
    order = alexander_module_order(G)
    
    metric_name = "alexander_module_order"
    metric_value = order
    instances_tested = 1
    n_max = n
    conjecture_holds = False if order > 2 * math.log(n / k) else True
    counterexample = "" if conjecture_holds else f"Order {order} exceeds 2 * log({n}/{k})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds 2 * log(n/k)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")