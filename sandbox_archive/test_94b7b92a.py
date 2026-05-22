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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def compute_lattice_rank(edges, n):
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        rank = 0
        for i in range(n):
            if any(adjacency_matrix[i][j] != 0 for j in range(i)):
                rank += 1
                for j in range(n):
                    if adjacency_matrix[j][i] != 0:
                        for k in range(n):
                            adjacency_matrix[j][k] -= adjacency_matrix[i][k]
        return rank
    
    def construct_quantum_circuit(rank, n):
        # Placeholder: This is a dummy function to simulate circuit construction
        # In practice, this would involve more complex logic.
        depth = rank ** 2
        return depth
    
    n = random.randint(5, 40)
    graph_edges = generate_graph(n)
    lattice_rank = compute_lattice_rank(graph_edges, n)
    
    if lattice_rank == 0:
        return {
            "metric_name": "Lattice Rank",
            "metric_value": lattice_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "lattice_rank_zero"
        }
    
    circuit_depth = construct_quantum_circuit(lattice_rank, n)
    
    expected_rank = round(n ** 1.5)
    within_factor = abs(lattice_rank - expected_rank) / expected_rank <= 0.5
    
    if not within_factor or circuit_depth > lattice_rank ** 2:
        return {
            "metric_name": "Lattice Rank vs Circuit Depth",
            "metric_value": lattice_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={lattice_rank}, depth={circuit_depth}"
        }
    
    return {
        "metric_name": "Lattice Rank vs Circuit Depth",
        "metric_value": lattice_rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(res["metric_value"] for res in results if "metric_value" in res)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results if "metric_value" in res) / len(results))
    
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        counterexample = next(res["counterexample"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")