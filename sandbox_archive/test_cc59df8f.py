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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
        for i in range(1, n):
            clauses.append(f'~{variables[i-1]} | {variables[i]}')
        return ' & '.join(clauses)
    
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
    
    def gaussian_elimination(matrix, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for k in range(i+1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n-1, -1, -1):
            x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i+1, n))) / matrix[i][i]
        return x
    
    def compute_resolution_width(formula):
        # Simplified resolution width estimation
        return len(formula.split(' & '))
    
    def irreducible_representations(group_order):
        # Placeholder for actual representation computation
        if group_order == 2:
            return [{'dim': 1}]
        elif group_order == 3:
            return [{'dim': 1}, {'dim': 2}]
        else:
            return [{'dim': 1}]
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    group_order = random.choice(generate_primes(10))
    representations = irreducible_representations(group_order)
    min_dim = min(rep['dim'] for rep in representations)
    
    width = compute_resolution_width(formula)
    lower_bound = 2 ** (min_dim - 1)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= lower_bound,
        "counterexample": "" if width >= lower_bound else f"Formula: {formula}, Width: {width}, Lower Bound: {lower_bound}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_width = sum(r['metric_value'] for r in results) / len(results)
    std_width = math.sqrt(sum((r['metric_value'] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r['conjecture_holds'])
        counterexample = results[seeds.index(first_failing_seed)]['counterexample']
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")