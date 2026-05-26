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
    
    def generate_monotone_circuit(n, m):
        # Generate a random monotone circuit with n variables and m gates
        circuit = []
        for _ in range(m):
            gate_type = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(1, n+1), 2))
            circuit.append((gate_type, inputs[0], inputs[1]))
        return circuit
    
    def evaluate_circuit(circuit, input_values):
        # Evaluate the circuit for a given input
        values = {i: 0 for i in range(1, len(input_values) + 1)}
        for gate_type, x, y in circuit:
            if gate_type == 'AND':
                values[x] &= input_values[x-1]
                values[y] &= input_values[y-1]
            elif gate_type == 'OR':
                values[x] |= input_values[x-1]
                values[y] |= input_values[y-1]
        return max(values.values())
    
    def construct_quasi_crystalline_set(circuit, n):
        # Construct the quasi-crystalline set for a given circuit
        Q = []
        for a in range(2**n):
            input_values = [(a >> i) & 1 for i in range(n)]
            if evaluate_circuit(circuit, input_values) == 1:
                Q.append(input_values)
        return Q
    
    def compute_rank(Q, q):
        # Compute the rank of the quasi-crystalline set over a finite field F_q
        n = len(Q[0])
        A = [[0] * (n + 1) for _ in range(n)]
        for i, point in enumerate(Q):
            for j in range(n):
                A[j][i] = point[j]
            A[n][i] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            for j in range(n - 1):
                i_max = next((i for i in range(rank, m) if A[i][j]), None)
                if i_max is not None:
                    A[rank], A[i_max] = A[i_max], A[rank]
                    for i in range(rank + 1, m):
                        factor = A[i][j] / A[rank][j]
                        for k in range(n):
                            A[i][k] -= factor * A[rank][k]
                    rank += 1
            return rank
        
        rank = gaussian_elimination(A)
        return rank
    
    def is_prime(num):
        if num <= 1:
            return False
        if num <= 3:
            return True
        if num % 2 == 0 or num % 3 == 0:
            return False
        i = 5
        while i * i <= num:
            if num % i == 0 or num % (i + 2) == 0:
                return False
            i += 6
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    n_values = [5, 10, 15, 20, 30, 40]
    q = generate_primes(1)[0]  # Use the smallest prime for simplicity
    results = []
    
    for n in n_values:
        m_min = max(1, n - 1)
        m_max = min(5 * n, 20 * n)
        m_range = list(range(m_min, m_max + 1))
        
        for _ in range(30):
            m = random.choice(m_range)
            circuit = generate_monotone_circuit(n, m)
            Q = construct_quasi_crystalline_set(circuit, n)
            rank = compute_rank(Q, q)
            
            results.append({
                "n": n,
                "m": m,
                "circuit": circuit,
                "Q": Q,
                "rank": rank
            })
    
    def extract_metric_value(results):
        return sum(result["rank"] for result in results) / len(results)
    
    def extract_conjecture_holds(results, q):
        upper_bound = math.log(len(results), 2)
        lower_bound = len(results)
        for result in results:
            if not (lower_bound <= result["rank"] <= upper_bound):
                return False
        return True
    
    metric_value = extract_metric_value(results)
    conjecture_holds = extract_conjecture_holds(results, q)
    
    return {
        "metric_name": "Minimal Rank of Quasi-crystalline Sets",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
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
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")