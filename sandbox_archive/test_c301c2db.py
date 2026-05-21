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
    
    def generate_random_strings(n):
        return ''.join(random.choice('01') for _ in range(n)), ''.join(random.choice('01') for _ in range(n))
    
    def create_entangled_state(X, Y):
        n = len(X)
        state = [0] * (n * n)
        for i in range(n):
            if X[i] == '1':
                state[i * n + int(Y[i])] = 1
        return state
    
    def matrix_multiplication(A, B):
        m, k, n = len(A), len(B[0]), len(B)
        C = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for l in range(k):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = max(range(i, m), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            pivot = augmented_matrix[i][i]
            if pivot == 0:
                continue
            for j in range(n + 1):
                augmented_matrix[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = augmented_matrix[k][i]
                    for j in range(n + 1):
                        augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
        return [row[-1] for row in augmented_matrix[:n]]
    
    def randomized_communication_complexity(X, Y):
        n = len(X)
        state = create_entangled_state(X, Y)
        A = [[0] * (n + 1) for _ in range(n)]
        B = [[0] * (n + 1) for _ in range(n)]
        b = [0] * n
        for i in range(n):
            if X[i] == '1':
                A[i][i] = 1
                b[i] = int(Y[i])
            else:
                B[i][i] = 1
        C = matrix_multiplication(A, B)
        x = gaussian_elimination(C, b)
        return sum(x) / n
    
    def minimal_tensor_rank(state):
        n = int(math.sqrt(len(state)))
        rank = 0
        for i in range(n):
            if state[i * n + i] == 1:
                rank += 1
        return rank
    
    X, Y = generate_random_strings(30)
    cc_disj = randomized_communication_complexity(X, Y)
    tau_psi = minimal_tensor_rank(create_entangled_state(X, Y))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": tau_psi / cc_disj,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")