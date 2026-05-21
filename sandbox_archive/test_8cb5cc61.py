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
    
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def generate_random_function(n):
        G = list(range(n))
        f = {}
        for g1 in G:
            for g2 in G:
                f[(g1, g2)] = random.choice([0, 1])
        return f
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def fourier_coefficient(f, pi, G):
        n = len(G)
        result = 0
        for g in G:
            result += f[(g, pi[g])]
        return result / n
    
    def communication_complexity(f, G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[(i, j)] == 1:
                    A[i][j] = 1
        b = [1] * n
        x = gaussian_elimination(A, b)
        return sum(x)
    
    def generate_irreducible_representations(n):
        representations = []
        for k in range(2, n // 2 + 1):
            if (n - 1) % k == 0:
                representation = [random.choice([1, -1]) for _ in range(k)]
                representations.append(representation)
        return representations
    
    G = list(range(4))
    f = generate_random_function(len(G))
    irreducible_representations = generate_irreducible_representations(len(G))
    
    max_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for pi in irreducible_representations:
        coefficient = fourier_coefficient(f, pi, G)
        if abs(coefficient) < 1 / math.log(len(G)):
            conjecture_holds = False
            counterexample = f"Non-trivial irreducible representation with |⟨π, f⟩| < 1/log(|G|)"
            break
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity(f, G),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if "metric_value" in r]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values)/len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")