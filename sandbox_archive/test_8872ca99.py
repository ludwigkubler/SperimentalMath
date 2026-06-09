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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0:
            return None
        graph = [[0] * n for _ in range(n)]
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if len(edges) == n * d // 2:
                    break
                if random.randint(0, 1) == 0 and (i, j) not in edges and (j, i) not in edges:
                    graph[i][j] = 1
                    graph[j][i] = 1
                    edges.add((i, j))
        return graph
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = Fraction(matrix[i][i])
            for j in range(n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(n):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def rank_variance(matrix):
        n = len(matrix)
        identity = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        augmented_matrix = [row + col for row, col in zip(matrix, identity)]
        reduced_matrix = gaussian_elimination(augmented_matrix)
        rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
        return n - rank
    
    def cohomological_complex(graph):
        n = len(graph)
        complex_ = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    complex_[i][j] = Fraction(1)
                    complex_[j][i] = Fraction(1)
        return complex_
    
    def second_betti_number(complex_):
        n = len(complex_)
        matrix = [[complex_[i][j] for j in range(i, n)] for i in range(n)]
        reduced_matrix = gaussian_elimination(matrix)
        rank = sum(1 for row in reduced_matrix if any(val != 0 for val in row))
        return n - rank
    
    def generate_graphs(n, d):
        graphs = []
        while len(graphs) < 30:
            graph = generate_d_regular_graph(n, d)
            if graph is not None and graph not in graphs:
                graphs.append(graph)
        return graphs
    
    def calculate_metric_value(graphs):
        total_variance = 0
        for graph in graphs:
            complex_ = cohomological_complex(graph)
            variance = rank_variance(complex_)
            total_variance += variance
        return total_variance / len(graphs)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        graphs = generate_graphs(n, 3)
        if not graphs:
            continue
        variance = calculate_metric_value(graphs)
        betti_number = second_betti_number(cohomological_complex(graphs[0]))
        results.append((variance, betti_number))
    
    if len(results) < 16:
        return {
            "metric_name": "rank_variance",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    variances = [result[0] for result in results]
    betti_numbers = [result[1] for result in results]
    mean_variance = sum(variances) / len(variances)
    mean_betti_number = sum(betti_numbers) / len(betti_numbers)
    support_fraction = sum(abs(v - b) <= 3 for v, b in zip(variances, betti_numbers)) / len(results)
    
    return {
        "metric_name": "rank_variance",
        "metric_value": mean_variance,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_variance = math.sqrt(sum((result["metric_value"] - mean_variance) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['instances_tested']}, variance={result['metric_value']}, betti_number={second_betti_number(cohomological_complex(generate_d_regular_graph(result['instances_tested'], 3)))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break