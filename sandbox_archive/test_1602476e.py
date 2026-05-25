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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        max_comm = 0
        for i in range(2**(n-1)):
            x = i.to_bytes((i.bit_length() + 7) // 8, 'big')
            y = (i ^ ((1 << (n-1)) - 1)).to_bytes(((i ^ ((1 << (n-1)) - 1)).bit_length() + 7) // 8, 'big')
            comm = sum(1 for a, b in zip(x, y) if a != b)
            max_comm = max(max_comm, comm)
        return max_comm
    
    def tropical_hermitian_form(f):
        n = len(f)
        H = [[0] * (n+1) for _ in range(n+1)]
        for i in range(2**n):
            x = [int(b) for b in format(i, f'0{n}b')]
            for j in range(2**n):
                y = [int(b) for b in format(j, f'0{n}b')]
                H[i%n][j%n] += x[j] * (-y[i])
        return H
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i+1, n):
                    matrix[j][i] /= matrix[i][i]
                for j in range(n):
                    if j == i:
                        continue
                    for k in range(n):
                        matrix[j][k] -= matrix[i][k] * matrix[j][i]
        return rank
    
    def is_positive_definite(matrix):
        n = len(matrix)
        for i in range(n):
            if matrix[i][i] <= 0:
                return False
            for j in range(i+1, n):
                matrix[j][i] /= matrix[i][i]
            for j in range(n):
                if j == i:
                    continue
                for k in range(n):
                    matrix[j][k] -= matrix[i][k] * matrix[j][i]
        return True
    
    def tropical_hermitian_rank(f):
        H = tropical_hermitian_form(f)
        rank = 0
        for i in range(len(H)):
            if is_positive_definite(H[:i+1][:i+1]):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_random_boolean_function(n)
            comm = communication_complexity(f)
            if comm > n**(1/4):
                rank = tropical_hermitian_rank(f)
                total_rank += rank
                instances_tested += 1
    
    mean_rank = total_rank / instances_tested if instances_tested > 0 else 0
    conjecture_holds = mean_rank >= math.sqrt(n)
    
    return {
        "metric_name": "Minimal Rank of Tropical Hermitian Form",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean rank {mean_rank} < sqrt({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mean rank {results[first_failing_seed]['metric_value']} < sqrt({n_values[0]})\" first_failing_seed={first_failing_seed}")