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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def symplectic_form_rank(A):
        m, n = len(A), len(A[0])
        if m != n or m % 2 != 0:
            raise ValueError("Matrix must be square and even-sized")
        B = [row[:n//2] + row[n//2:] for row in A]
        C = [[A[i][j] - A[i+n//2][j+n//2] for j in range(n)] for i in range(m)]
        return max(gaussian_elimination(B), gaussian_elimination(C))
    
    def read_twice_branching_program(size):
        if size == 1:
            return [0]
        else:
            left = read_twice_branching_program(size // 2)
            right = read_twice_branching_program(size - size // 2)
            return [left, right]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_rank = 0
        
        for _ in range(5):
            circuit_size = random.randint(1, n)
            circuit = read_twice_branching_program(circuit_size)
            rank = symplectic_form_rank(circuit)
            instances_tested += 1
            total_rank += rank
        
        mean_rank = total_rank / instances_tested
        expected_rank = math.log2(n) ** 2
        ratio = mean_rank / expected_rank
        
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "mean_rank": mean_rank,
            "expected_rank": expected_rank,
            "ratio": ratio
        })
    
    conjecture_holds = all(0.7 <= result["ratio"] <= 1.3 for result in results)
    counterexample = "" if conjecture_holds else "n={}".format(results[0]["n"])
    
    return {
        "metric_name": "Symplectic Form Rank vs BP_ReadTwice Circuit Depth",
        "metric_value": mean_rank,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_rank = sum(result["mean_rank"] * result["instances_tested"] for result in results) / sum(result["instances_tested"] for result in results)
    expected_rank = math.log2(sum(result["n"] for result in results)) ** 2
    support_fraction = sum(1 for result in results if 0.7 <= result["ratio"] <= 1.3) / len(results)
    
    if all(0.7 <= result["ratio"] <= 1.3 for result in results):
        print("RESULT: SUPPORTED mean={:.2f} std=NA support_fraction={:.2f}".format(mean_rank, support_fraction))
    elif any(not 0.7 <= result["ratio"] <= 1.3 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not (0.7 <= result["ratio"] <= 1.3))
        print("RESULT: FALSIFIED counterexample='n={}' first_failing_seed={}".format(results[0]["n"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")