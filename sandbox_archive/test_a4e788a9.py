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
    
    def generate_boolean_circuit(depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return random.choice([left and right, left or right])
    
    def tropicalize(circuit):
        if isinstance(circuit, int):
            return circuit
        elif isinstance(circuit, list):
            return max(tropicalize(circuit[0]), tropicalize(circuit[1]))
        else:
            raise ValueError("Invalid circuit")
    
    def rank_tropicalized_scheme(scheme):
        n = len(scheme)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if scheme[i] == scheme[j]:
                    matrix[i][j] = 1
                    matrix[j][i] = 1
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(n):
                    if row[i]:
                        for j in range(n):
                            matrix[j][i] -= matrix[j][row.index(1)]
        return rank
    
    def generate_and_or_tree(depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            left = generate_and_or_tree(depth - 1)
            right = generate_and_or_tree(depth - 1)
            return (left, right) if random.choice([True, False]) else (left or right, left and right)
    
    def compute_rank_from_depth(depth):
        return 2 ** (depth // 2)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit_size = 2 ** n
        depth = int(math.log2(circuit_size))
        
        if depth < 2:
            continue
        
        circuit = generate_boolean_circuit(depth)
        tropicalized_scheme = tropicalize(circuit)
        rank = rank_tropicalized_scheme(tropicalized_scheme)
        
        expected_rank = compute_rank_from_depth(depth)
        
        results.append({
            "circuit_size": circuit_size,
            "depth": depth,
            "rank": rank,
            "expected_rank": expected_rank
        })
    
    if not results:
        return {
            "metric_name": "Rank vs Circuit Size",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    ranks = [result["rank"] for result in results]
    expected_ranks = [result["expected_rank"] for result in results]
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        sorted_indices1 = sorted(range(n), key=lambda i: ranks1[i])
        sorted_indices2 = sorted(range(n), key=lambda i: ranks2[i])
        rank_diffs_squared = sum((sorted_indices1[i] - sorted_indices2[i]) ** 2 for i in range(n))
        return 1 - (6 * rank_diffs_squared) / (n * (n**2 - 1))
    
    correlation = spearman_correlation(ranks, expected_ranks)
    
    return {
        "metric_name": "Rank vs Circuit Size",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.8,
        "counterexample": "" if correlation >= 0.5 else f"Correlation {correlation} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 37))  # Default to first 30 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation below 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")