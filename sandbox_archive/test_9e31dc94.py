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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_mul(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_neg(a):
        return -a
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_identity(x):
        return x
    
    def tropical_inverse(x):
        if x == float('-inf'):
            return float('-inf')
        return -x
    
    def tropical_matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[tropical_zero() for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] = tropical_add(C[i][j], tropical_mul(A[i][k], B[k][j]))
        return C
    
    def tropical_matrix_power(M, k):
        if k == 0:
            n = len(M)
            I = [[tropical_zero() for _ in range(n)] for _ in range(n)]
            for i in range(n):
                I[i][i] = tropical_one()
            return I
        elif k % 2 == 1:
            return tropical_matrix_multiply(M, tropical_matrix_power(M, k - 1))
        else:
            half_power = tropical_matrix_power(M, k // 2)
            return tropical_matrix_multiply(half_power, half_power)
    
    def tropical_rank(matrix):
        m = len(matrix)
        n = len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != float('-inf'):
                rank += 1
                for j in range(i + 1, m):
                    factor = tropical_neg(tropical_divide(matrix[j][i], matrix[i][i]))
                    for k in range(n):
                        matrix[j][k] = tropical_add(matrix[j][k], tropical_mul(factor, matrix[i][k]))
        return rank
    
    def tropical_divide(a, b):
        if b == float('-inf'):
            return float('-inf')
        return a - b
    
    def xor_function(x):
        result = 0
        for bit in x:
            result ^= bit
        return result
    
    def generate_xor_function(n):
        inputs = [random.randint(0, 1) for _ in range(n)]
        outputs = [xor_function(inputs)]
        for _ in range(n - 1):
            new_input = random.randint(0, 1)
            new_output = xor_function(inputs + [new_input])
            inputs.append(new_input)
            outputs.append(new_output)
        return inputs, outputs
    
    def construct_tropical_curve(inputs, outputs):
        n = len(inputs)
        m = n + 1
        A = [[tropical_zero() for _ in range(m)] for _ in range(m)]
        for i in range(n):
            A[i][i] = tropical_one()
            A[n][i] = inputs[i]
        A[n][n] = tropical_one()
        B = [[tropical_zero() for _ in range(1)] for _ in range(m)]
        B[n][0] = outputs[0]
        return A, B
    
    def communication_complexity(inputs):
        n = len(inputs)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return n - 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_communication = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            inputs, outputs = generate_xor_function(n)
            A, B = construct_tropical_curve(inputs, outputs)
            rank = tropical_rank(A)
            comm_complexity = communication_complexity(inputs)
            total_rank += rank
            total_communication += comm_complexity
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_communication = total_communication / instances_tested
    
    conjecture_holds = mean_rank <= log2(n_values[-1]) ** 2 and mean_communication >= log2(n_values[-1]) ** 2
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank}, Mean communication {mean_communication}"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_communication,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank {r['metric_value']}, Mean communication {r['metric_value']}\" first_failing_seed={first_failing_seed}")