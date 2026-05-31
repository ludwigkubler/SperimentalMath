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
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def circuit_satisfiability_time(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function of n variables")
        
        count = 0
        for i in range(2**n):
            if all(f[i ^ j] == f[j] for j in range(n)):
                count += 1
        return count
    
    def permutation_group_size(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function of n variables")
        
        group = set()
        for i in range(2**n):
            for j in range(n):
                if f[i ^ (1 << j)] == f[j]:
                    group.add((i, j))
        return len(group)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiplication(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0] * k for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        Augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                    max_row = j
            Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
            if Augmented[i][i] == 0:
                raise ValueError("No unique solution exists")
            for j in range(i+1, m):
                factor = Augmented[j][i] / Augmented[i][i]
                for k in range(n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (Augmented[i][-1] - sum(Augmented[i][j] * x[j] for j in range(i+1, n))) / Augmented[i][i]
        return x
    
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def generate_primes(n):
        primes = []
        candidate = 2
        while len(primes) < n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes
    
    def random_sample(population, k):
        if k > len(population):
            raise ValueError("Sample larger than population or is negative")
        sample = []
        for _ in range(k):
            index = random.randint(0, len(population) - 1)
            sample.append(population.pop(index))
        return sample
    
    def mean(values):
        return sum(values) / len(values)
    
    def std_dev(values, mean_val):
        return math.sqrt(sum((x - mean_val) ** 2 for x in values) / len(values))
    
    def correlation_coefficient(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("Both lists must have the same length")
        
        mean_x = mean(x)
        mean_y = mean(y)
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = std_dev(x, mean_x) * std_dev(y, mean_y)
        return numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            t_f = circuit_satisfiability_time(f)
            G_f = permutation_group_size(f)
            
            if t_f == 0:
                continue
            
            results.append({
                "n": n,
                "t_f": t_f,
                "G_f": G_f
            })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x = [result["t_f"] for result in results]
    y = [result["G_f"] for result in results]
    
    mean_x = mean(x)
    mean_y = mean(y)
    corr_coeff = correlation_coefficient(x, y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_coeff,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(corr_coeff) > 0.1,  # Threshold for significance
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not significant\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = mean([result["metric_value"] for result in results])
        std_value = std_dev([result["metric_value"] for result in results], mean_value)
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")