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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def geometric_lattice_rank(edges, n):
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adjacency_matrix[u][v] = 1
            adjacency_matrix[v][u] = 1
        
        # Gaussian elimination to find rank
        rank = 0
        for i in range(n):
            if all(adjacency_matrix[j][i] == 0 for j in range(rank)):
                continue
            pivot_row = rank
            while adjacency_matrix[pivot_row][i] == 0:
                pivot_row += 1
                if pivot_row == n:
                    return rank
            for j in range(n):
                if j != i:
                    factor = Fraction(adjacency_matrix[j][i], adjacency_matrix[i][i])
                    for k in range(n):
                        adjacency_matrix[j][k] -= factor * adjacency_matrix[i][k]
            rank += 1
        return rank
    
    def quantum_circuit_depth(rank):
        # Simplified model: depth is proportional to rank^2
        return rank ** 2
    
    n = random.randint(5, 40)
    graph_edges = generate_graph(n)
    lattice_rank = geometric_lattice_rank(graph_edges, n)
    circuit_depth = quantum_circuit_depth(lattice_rank)
    
    metric_name = "Lattice Rank vs. Circuit Depth"
    metric_value = lattice_rank / (n ** 1.5)
    instances_tested = 1
    conjecture_holds = abs(metric_value - 1) < 0.75 and circuit_depth <= lattice_rank ** 2 * 4
    counterexample = "" if conjecture_holds else f"Graph with n={n}, rank={lattice_rank}, depth={circuit_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")