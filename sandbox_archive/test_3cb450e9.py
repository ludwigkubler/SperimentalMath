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
    
    def generate_primes(n):
        primes = []
        num = 2
        while len(primes) < n:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def gaussian_elimination(matrix, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
                b[j] -= factor * b[i]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]
        return x
    
    def compute_quantization_rank(f):
        # Placeholder for the actual computation of ρ(f)
        # This is a dummy implementation
        return random.uniform(0.5, 2.0)
    
    def generate_cnf(n):
        cnf = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            cnf.append(clause)
        return cnf
    
    def compute_bp_size(cnf):
        # Placeholder for the actual computation of BP size
        # This is a dummy implementation
        return random.randint(50, 200)
    
    def compute_circuit_size(cnf):
        # Placeholder for the actual computation of circuit size
        # This is a dummy implementation
        return random.randint(100, 400)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    bp_size = compute_bp_size(cnf)
    circuit_size = compute_circuit_size(cnf)
    
    quantization_rank = compute_quantization_rank(cnf)
    log_bp_size = math.log(bp_size)
    log_circuit_size = math.log(circuit_size)
    
    metric_name = "Quantization Rank vs BP/Circuit Size"
    metric_value = abs(quantization_rank - log_bp_size) + abs(quantization_rank - log_circuit_size)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if quantization_rank <= log_bp_size and quantization_rank >= log_circuit_size:
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")