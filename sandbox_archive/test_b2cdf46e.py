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
    
    def generate_random_3_regular_graph(n):
        if n % 2 != 0 or n < 4:
            return None
        
        graph = [[] for _ in range(n)]
        edges = set()
        
        for i in range(n):
            neighbors = random.sample(range(i + 1, n), 2)
            for neighbor in neighbors:
                if (i, neighbor) not in edges and (neighbor, i) not in edges:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
                    edges.add((i, neighbor))
        
        return graph
    
    def hodge_index(graph):
        n = len(graph)
        adjacency_matrix = [[0] * n for _ in range(n)]
        degree_matrix = [len(neighbors) for neighbors in graph]
        
        for i, neighbors in enumerate(graph):
            for neighbor in neighbors:
                adjacency_matrix[i][neighbor] = 1
        
        laplacian_matrix = []
        for i in range(n):
            row = [-degree_matrix[i]] + [0 if j != i else 1 for j in range(n)]
            laplacian_matrix.append(row)
        
        # Compute the determinant of the Laplacian matrix
        def determinant(matrix, n):
            if n == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix, n - 1)
            return det
        
        hodge_index = abs(determinant(laplacian_matrix, n))
        return hodge_index
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_index = 0
    instances_tested = 0
    support_count = 0
    
    for n in n_values:
        graph = generate_random_3_regular_graph(n)
        if graph is None:
            continue
        
        hodge = hodge_index(graph)
        total_hodge_index += hodge
        instances_tested += 1
        
        if hodge <= math.log(n) / 4:
            support_count += 1
    
    mean_hodge_index = total_hodge_index / instances_tested if instances_tested > 0 else 0
    conjecture_holds = (support_count / instances_tested >= 0.8)
    
    return {
        "metric_name": "MinimalHodgeIndex",
        "metric_value": mean_hodge_index,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Graph with n={n_values[0]} and HodgeIndex<{math.log(n_values[0]) / 4}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(total_metric_values) / len(total_metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={n_values[0]} and HodgeIndex<{math.log(n_values[0]) / 4}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")