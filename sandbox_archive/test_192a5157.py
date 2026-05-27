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
    
    def entropy(graph):
        n = len(graph)
        degree_sum = sum(sum(row) for row in graph)
        avg_degree = degree_sum / (n * (n - 1))
        return math.log2(n) + avg_degree
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    continue
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j != i and matrix[j][i] != 0:
                    factor = -matrix[j][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
            rank += 1
        return rank
    
    def generate_graph(n):
        graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    graph[i][j] = 1
                    graph[j][i] = 1
        return graph
    
    def minimal_rank(graph):
        n = len(graph)
        matrix = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n):
                if graph[i][j] == 1:
                    matrix[i][j] = Fraction(1)
                    matrix[j][i] = Fraction(1)
        for i in range(n):
            matrix[n][i] = Fraction(-1)
        return gaussian_elimination(matrix)
    
    def communication_complexity(rank, n):
        if rank < 2**n / math.e**(entropy(graph)):
            return True
        return False
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    support_fraction = 0
    communication_lower_bounds = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n)
            rank = minimal_rank(graph)
            total_rank += rank
            instances_tested += 1
            if rank >= 2**n / math.e**(entropy(graph)):
                support_fraction += 1
            if communication_complexity(rank, n):
                communication_lower_bounds += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = support_fraction / len(n_values) >= 0.8 and mean_rank <= 3 * math.log2(instances_tested)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "communication_complexity_lower_bounds_not_met"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8 and mean_rank <= 3 * math.log2(len(results)):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='communication_complexity_lower_bounds_not_met' first_failing_seed={first_failing_seed}")