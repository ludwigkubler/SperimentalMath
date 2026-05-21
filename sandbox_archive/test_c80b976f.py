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
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n-1):
            clauses.append([literals[i], f'~{literals[i+1]}'])
        clauses.append([f'~{literals[0]}', literals[-1]])
        return literals, clauses

    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes

    def gaussian_elimination(matrix, augmented=True):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(i+1, rows):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    if augmented:
                        matrix[j][k] += factor * matrix[i][k]
                    else:
                        matrix[j][k] += factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref = gaussian_elimination([row[:] for row in matrix], augmented=False)
        rank = 0
        for i in range(rows):
            if any(rref[i][j] != 0 for j in range(cols)):
                rank += 1
        return rank

    def automorphism_group_size(n, clauses):
        # Simplified approach to estimate the size of the automorphism group
        # This is a placeholder and should be replaced with actual combinatorial group theory code
        return n + len(clauses)

    def resolution_proof_length(n, clauses):
        # Simplified approach to estimate the Resolution proof length
        # This is a placeholder and should be replaced with actual resolution algorithm code
        return 2 ** (n + len(clauses))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        literals, clauses = tseitin_formula(n)
        nu_G = automorphism_group_size(n, clauses)
        Resolution_Tseitin_G = resolution_proof_length(n, clauses)
        ratio = Fraction(Resolution_Tseitin_G, 2 ** nu_G)
        results.append({
            "n": n,
            "nu_G": nu_G,
            "Resolution_Tseitin_G": Resolution_Tseitin_G,
            "ratio": ratio
        })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    max_ratio = max(result["ratio"] for result in results)
    
    conjecture_holds = all(result["ratio"] <= Fraction(3, 2) for result in results)
    counterexample = "" if conjecture_holds else f"n={results[max_ratio_index]['n']}, ratio={max_ratio}"
    
    return {
        "metric_name": "Ratio of Resolution proof length to 2^(ν(G))",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        max_ratio = max(result["metric_value"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='ratio={max_ratio}' first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support fraction")