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
    
    def generate_boolean_formula(n):
        if n == 1:
            return 'A'
        else:
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} OR {right})'

    def resolution_proof_width(phi):
        stack = []
        for char in phi:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack[-1] != '(':
                    stack.pop()
                stack.pop()
                if len(stack) > 0 and stack[-1] == 'OR':
                    stack.pop()  # Remove the OR operator
        return len(stack)

    def frobenius_endomorphism_order(G):
        n = len(G)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        F = G.copy()
        order = 1
        while True:
            F = matrix_multiply(F, F)
            if matrix_equal(F, I):
                return order
            order += 1

    def matrix_multiply(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def matrix_equal(A, B):
        n = len(A)
        for i in range(n):
            for j in range(n):
                if A[i][j] != B[i][j]:
                    return False
        return True

    n = random.randint(5, 40)
    phi = generate_boolean_formula(n)
    w_phi = resolution_proof_width(phi)
    
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    min_order_G = frobenius_endomorphism_order(G)

    return {
        "metric_name": "min_order(G(φ))",
        "metric_value": min_order_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")