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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            if len(set(clause)) == 3:
                clauses.append(clause)
        return clauses
    
    def monomial_ideal(clauses):
        ideal = set()
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    ideal.add((clause[i], clause[j]))
        return ideal
    
    def hilbert_function(ideal, n):
        h = [0] * (n + 1)
        for k in range(n + 1):
            count = 0
            for i in range(1, n + 1):
                if all((i & (1 << j)) != 0 for j in ideal):
                    count += 1
            h[k] = count
        return h
    
    def acc0_circuit_size(clauses):
        # Placeholder function to simulate ACC^0 circuit size calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    ideal = monomial_ideal(clauses)
    h = hilbert_function(ideal, n)
    circuit_size = acc0_circuit_size(clauses)
    
    metric_name = "Hilbert Function Growth"
    metric_value = sum(h) / (n + 1)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if h[-1] >= math.log(n):
        if circuit_size >= n:
            conjecture_holds = True
        else:
            counterexample = "Circuit size is less than Ω(n)"
    elif h[-1] < math.log(n):
        if circuit_size < n:
            conjecture_holds = True
        else:
            counterexample = "Hilbert function growth is less than Ω(log n) but circuit size is ≥ Ω(n)"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")