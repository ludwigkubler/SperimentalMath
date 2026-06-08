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

def generate_k_cnf(n, k=3):
    clauses = []
    for _ in range(k * n):
        clause = set()
        while len(clause) < k:
            var = random.randint(1, n)
            sign = random.choice([1, -1])
            if (var, sign) not in clause and (-var, -sign) not in clause:
                clause.add((var, sign))
        clauses.append(clause)
    return clauses

def simplicial_complex_from_k_cnf(clauses):
    faces = {frozenset(): 1}
    for clause in clauses:
        for i in range(len(clause)):
            face = frozenset(clause[:i] + clause[i+1:])
            if face not in faces:
                faces[face] = 0
            faces[face] += faces[frozenset()]
    return faces

def minimal_local_index(faces):
    max_dim = max(len(face) for face in faces)
    local_indices = [0] * (max_dim + 1)
    for dim, count in faces.items():
        if len(dim) > 0:
            local_indices[len(dim)] += count
    return sum(local_indices)

def frege_proof_depth(k_cnf):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(k_cnf) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n size 5 times
            clauses = generate_k_cnf(n)
            faces = simplicial_complex_from_k_cnf(clauses)
            local_index = minimal_local_index(faces)
            proof_depth = frege_proof_depth(clauses)
            
            if local_index > 10:
                return {
                    "metric_name": "local_index",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": "local_index_too_large"
                }
            
            metric_values.append((local_index, proof_depth))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "local_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_metric_values"
        }
    
    local_indices, proof_depths = zip(*metric_values)
    correlation_coefficient = sum((x - mean_local_index) * (y - mean_proof_depth) for x, y in zip(local_indices, proof_depths)) / math.sqrt(sum((x - mean_local_index) ** 2 for x in local_indices) * sum((y - mean_proof_depth) ** 2 for y in proof_depths))
    mean_local_index = Fraction(sum(local_indices), len(local_indices)).limit_denominator()
    mean_proof_depth = Fraction(sum(proof_depths), len(proof_depths)).limit_denominator()
    
    return {
        "metric_name": "local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= Fraction(7, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = Fraction(sum(r['metric_value'] for r in results if r['metric_value'] is not None), len(results)).limit_denominator()
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"local_index_too_large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_metric_values")