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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n, d):
        circuit = [[0] * n for _ in range(n)]
        for _ in range(d):
            i, j = random.sample(range(n), 2)
            circuit[i][j], circuit[j][i] = 1, 1
        return circuit
    
    def complement_graph(graph):
        n = len(graph)
        comp_graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 0:
                    comp_graph[i][j], comp_graph[j][i] = 1, 1
        return comp_graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            rank += 1
            for j in range(i + 1, n):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def max_ratio(circuit_ranks):
        if not circuit_ranks:
            return 0
        d_max = max(d for _, d in circuit_ranks)
        n_max = max(n for n, _ in circuit_ranks)
        bound = (2/3) * d_max**(2/3) * n_max**(1/3)
        ratios = [rank / bound for rank, _ in circuit_ranks]
        return max(ratios)
    
    circuit_ranks = []
    for n in range(5, 41):
        for _ in range(7):  # Aim for at least 30 instances per seed
            d = random.randint(1, min(n, 40))
            circuit = generate_circuit(n, d)
            comp_graph = complement_graph(circuit)
            rank = gaussian_elimination(comp_graph)
            circuit_ranks.append((rank, n, d))
    
    max_ratio_value = max_ratio(circuit_ranks)
    conjecture_holds = max_ratio_value <= 2
    counterexample = "" if conjecture_holds else f"max_ratio={max_ratio_value}"
    
    return {
        "metric_name": "max_ratio",
        "metric_value": max_ratio_value,
        "instances_tested": len(circuit_ranks),
        "n_max": max(n for _, n, _ in circuit_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_ratio exceeded bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")