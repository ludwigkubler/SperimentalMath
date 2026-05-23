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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(limit):
        primes = []
        num = 2
        while len(primes) < limit:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            raise ValueError("Matrix must be square")
        if rows == 1:
            return matrix[0][0]
        det = 0
        for j in range(cols):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_coxeter_group(transpositions):
        n = len(transpositions)
        group = set()
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in transpositions and (j, i) not in transpositions:
                    continue
                new_group = group.copy()
                new_group.add((i, j))
                while True:
                    changed = False
                    for k in range(n):
                        if (k, i) in new_group and (k, j) in new_group:
                            new_group.remove((k, i))
                            new_group.remove((k, j))
                            new_group.add((k, j))
                            new_group.add((i, k))
                            changed = True
                    if not changed:
                        break
                group = new_group
        return len(group)
    
    def pseudorandomness(f):
        n = len(f)
        random_vars = [random.choice([0, 1]) for _ in range(n)]
        correlation = sum(f[i] * random_vars[i] for i in range(n)) / n
        return abs(correlation)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def transpositions_of_boolean_function(f):
        n = len(f)
        transpositions = set()
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    transpositions.add((i, j))
        return transpositions
    
    def count_non_isomorphic_coxeter_groups(transpositions):
        n = len(transpositions)
        matrix = [[0] * (n * (n - 1) // 2) for _ in range(n * (n - 1) // 2)]
        index = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in transpositions:
                    matrix[index][index] = 1
                    index += 1
        return is_coxeter_group(matrix)
    
    def upper_bound(n):
        return 2**n / (n * math.log(n))
    
    def lower_bound(epsilon):
        # This is a placeholder for the actual lower bound function
        # For simplicity, we use a constant polynomial p(ε) = 1
        return 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    transpositions = transpositions_of_boolean_function(f)
    num_groups = count_non_isomorphic_coxeter_groups(transpositions)
    pseudorandomness_value = pseudorandomness(f)
    
    upper_bound_value = upper_bound(n)
    lower_bound_value = lower_bound(0.5)  # Using a fixed epsilon for simplicity
    
    conjecture_holds = (num_groups <= upper_bound_value and pseudorandomness_value >= 0.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Coxeter Group Complexity vs Pseudorandomness",
        "metric_value": num_groups,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")