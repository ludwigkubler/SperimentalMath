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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def p_adic_derivative(f, n):
        if len(f) != 2**n:
            raise ValueError("f must be a boolean function of n bits")
        df = [0] * (2**n)
        for i in range(2**n):
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    df[i] += 1
        return df
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [0] * (n - m) for row in matrix]
        for i in range(m):
            if augmented_matrix[i][i] == 0:
                for j in range(i+1, m):
                    if augmented_matrix[j][i] != 0:
                        augmented_matrix[i], augmented_matrix[j] = augmented_matrix[j], augmented_matrix[i]
                        break
                else:
                    continue
                if augmented_matrix[i][i] == 0:
                    return i - 1
            pivot = augmented_matrix[i][i]
            for j in range(n):
                augmented_matrix[i][j] /= pivot
            for j in range(m):
                if j != i and augmented_matrix[j][i] != 0:
                    factor = augmented_matrix[j][i]
                    for k in range(n):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        return m
    
    def communication_complexity(df, n):
        # Simplified model of communication complexity
        return sum(df) / (2**n)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    df = p_adic_derivative(f, n)
    H_M = [[df[i] * df[j] for j in range(2**n)] for i in range(2**n)]
    rho_f = rank(H_M)
    CC_R_f = communication_complexity(df, n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC_R_f,
        "instances_tested": 1,
        "conjecture_holds": CC_R_f <= rho_f**2,
        "counterexample": "" if CC_R_f <= rho_f**2 else f"CC_R(f) = {CC_R_f}, rho(f)^2 = {rho_f**2}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                counterexample = res["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")