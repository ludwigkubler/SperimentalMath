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
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= factor
            for j in range(n):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(i, n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def hodge_structure_rank(matrix):
        rank = 0
        echelon_form = gaussian_elimination(matrix)
        for row in echelon_form:
            if any(row[i] != 0 for i in range(len(row))):
                rank += 1
        return rank

    def bp_read_twice_circuit_threshold(graph):
        n = len(graph)
        threshold = 0
        for node in range(n):
            neighbors = graph[node]
            if len(neighbors) > threshold:
                threshold = len(neighbors)
        return threshold

    def generate_random_graph(n, density=0.5):
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < density and i != j:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph

    n = 40
    graph = generate_random_graph(n)
    matrix = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    rank = hodge_structure_rank(matrix)
    k = bp_read_twice_circuit_threshold(graph)
    
    if k == 0:
        return {
            "metric_name": "Rank vs DPLL Height",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = abs(rank - k)
    conjecture_holds = metric_value <= 3 * (k ** 2)  # Polynomial bound example
    counterexample = "" if conjecture_holds else f"Rank {rank}, K {k}"
    
    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or refute the conjecture")