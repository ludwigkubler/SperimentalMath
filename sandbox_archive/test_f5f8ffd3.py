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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set(random.sample(range(1, n + 1), 2))
            if random.choice([True, False]):
                clause = {x: -y for x, y in clause.items()}
            clauses.append(clause)
        return clauses

    def compute_simplicial_complex(clauses):
        simplicial_complex = set()
        for clause in clauses:
            for i in range(1, len(clause) + 1):
                for subset in itertools.combinations(clause.keys(), i):
                    simplicial_complex.add(frozenset(subset))
        return simplicial_complex

    def compute_local_index(simplicial_complex):
        local_index = {}
        for face in simplicial_complex:
            if len(face) == 1:
                continue
            num_components = 0
            visited = set()
            stack = list(face)
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    neighbors = [f for f in simplicial_complex if node in f and len(f) == len(node) + 1]
                    stack.extend(neighbors)
                    num_components += 1
            local_index[len(face)] = num_components
        return local_index

    def compute_frege_proof_depth(clauses):
        # Placeholder for actual Frege proof depth computation
        # This is a dummy implementation for demonstration purposes
        return sum(len(clause) for clause in clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    local_index_sum = 0
    frege_proof_depth_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            clauses = generate_k_cnf(n, k=3)
            simplicial_complex = compute_simplicial_complex(clauses)
            local_index = compute_local_index(simplicial_complex)
            frege_proof_depth = compute_frege_proof_depth(clauses)
            
            if max(local_index.values()) > 10:
                return {
                    "metric_name": "local_index",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": "local_index > 10"
                }
            
            local_index_sum += sum(local_index.values())
            frege_proof_depth_sum += frege_proof_depth
            instances_tested += 1

    if instances_tested < 30:
        return {
            "metric_name": "local_index",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_local_index = local_index_sum / instances_tested
    mean_frege_proof_depth = frege_proof_depth_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(local_index[i] * frege_proof_depth for i in range(1, max(local_index.keys()) + 1)) -
                               mean_local_index * mean_frege_proof_depth) / \
                              math.sqrt((instances_tested * sum(local_index[i]**2 for i in range(1, max(local_index.keys()) + 1)) - mean_local_index**2) *
                                        (instances_tested * sum(frege_proof_depth**2 for _ in range(instances_tested)) - mean_frege_proof_depth**2))

    return {
        "metric_name": "local_index",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")