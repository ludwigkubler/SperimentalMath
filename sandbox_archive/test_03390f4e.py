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
    
    def communication_matrix_rank(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i ^ (1 << j)] - f[i] for j in range(n)] for i in range(2**n)]
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
                for i in range(len(matrix)):
                    if matrix[i][0]:
                        factor = matrix[i][0] / row[0]
                        for j in range(len(row)):
                            matrix[i][j] -= factor * row[j]
        return rank
    
    def vector_bundle_rank(f):
        n = int(math.log2(len(f)))
        # Construct a transition map (simplified example)
        transition_map = {}
        for i in range(2**n):
            for j in range(n):
                if f[i ^ (1 << j)] != f[i]:
                    if i not in transition_map:
                        transition_map[i] = []
                    transition_map[i].append(j)
        # Compute the rank of the vector bundle
        rank = 0
        visited = set()
        for node in range(2**n):
            if node not in visited:
                rank += 1
                stack = [node]
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        for neighbor in transition_map.get(current, []):
                            stack.append(current ^ (1 << neighbor))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        vector_rank = vector_bundle_rank(f)
        comm_rank = communication_matrix_rank(f)
        results.append((vector_rank, comm_rank))
    
    if len(results) < 100:
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    vector_ranks = [r[0] for r in results]
    comm_ranks = [r[1] for r in results]
    
    mean_vector_rank = sum(vector_ranks) / len(vector_ranks)
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    
    if not (0.5 <= mean_vector_rank / mean_comm_rank <= 2):
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "out_of_range"
        }
    
    correlation = sum((vector_ranks[i] - mean_vector_rank) * (comm_ranks[i] - mean_comm_rank) for i in range(len(vector_ranks))) / len(vector_ranks)
    if abs(correlation) < 0.7:
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "low_correlation"
        }
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": mean_vector_rank / mean_comm_rank,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / supported_count
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / supported_count
    
    support_fraction = supported_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")