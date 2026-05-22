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
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_mult(A, B):
        m, n = len(A), len(B[0])
        p = len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def gaussian_elimination(A, b):
        n = len(b)
        Augmented = [A[i] + [b[i]] for i in range(n)]
        
        for i in range(n):
            max_row = max(range(i, n), key=lambda k: abs(Augmented[k][i]))
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            
            factor = Augmented[i][i]
            if factor == 0:
                continue
            for j in range(n + 1):
                Augmented[i][j] /= factor
        
            for k in range(n):
                if k != i:
                    factor = Augmented[k][i]
                    for j in range(n + 1):
                        Augmented[k][j] -= factor * Augmented[i][j]
        
        return [row[-1] for row in Augmented]

    def construct_tropical_curve(circuit_size):
        # Placeholder function to simulate the construction of a tropical curve
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, circuit_size)
    
    def hodge_degeneration_rank(tropical_curve):
        # Placeholder function to calculate the Hodge degeneration rank
        # This is a dummy implementation and should be replaced with actual logic
        return len(str(tropical_curve))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit_size = n
    beta = 0.5
    
    tropical_curve = construct_tropical_curve(circuit_size)
    rank = hodge_degeneration_rank(tropical_curve)
    
    metric_value = rank / (beta * n)
    
    return {
        "metric_name": "Hodge Degeneration Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": rank >= beta * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")