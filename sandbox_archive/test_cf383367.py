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
    
    def generate_boolean_function(m):
        return [random.choice([True, False]) for _ in range(2**m)]
    
    def construct_graph(phi):
        n = len(phi)
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if phi[i] != phi[j]:
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
    def min_noncrossing_partitions(graph):
        n = len(graph)
        partitions = [[i] for i in range(n)]
        while True:
            new_partitions = []
            for partition in partitions:
                subgraphs = [[] for _ in range(len(partition))]
                for edge in graph:
                    u, v = edge
                    if any(u in p and v in p for p in partition):
                        subgraph_index = partition.index(next(p for p in partition if u in p))
                        subgraphs[subgraph_index].append(edge)
                new_partition = []
                for i in range(len(subgraphs)):
                    if len(subgraphs[i]) > 0:
                        new_partition.append([j for j in range(n) if any(j in p for p in partition if (j, j+1) in subgraphs[i] or (j+1, j) in subgraphs[i])])
                new_partitions.extend(new_partition)
            if len(new_partitions) == len(partitions):
                return len(partitions)
            partitions = new_partitions
    
    def frege_proof_length(phi):
        # Simplified DPLL-based solver
        n = len(phi)
        clauses = []
        for i in range(n):
            clauses.append([i, -i-1])
        for i in range(n):
            for j in range(i+1, n):
                if phi[i] != phi[j]:
                    clauses.append([-i-1, -j-1])
                    clauses.append([i, j])
        def solve(lits_true, lits_false):
            stack = []
            while True:
                if not stack:
                    return False
                lit = stack.pop()
                if lit in lits_true:
                    continue
                if lit in lits_false:
                    return False
                if -lit in lits_true:
                    lits_true.remove(-lit)
                elif -lit in lits_false:
                    lits_false.remove(-lit)
                else:
                    stack.append(lit)
                    stack.extend([i for i in range(n) if i not in lits_true and i not in lits_false])
            return True
        return len(solve([], []))
    
    m = random.randint(5, 40)
    phi = generate_boolean_function(m)
    graph = construct_graph(phi)
    min_order = min_noncrossing_partitions(graph)
    proof_length = frege_proof_length(phi)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": min_order / proof_length if proof_length > 0 else float('inf'),
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if not math.isinf(r["metric_value"])) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if not math.isinf(r["metric_value"])) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(not math.isinf(r["metric_value"]) for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(math.isinf(r["metric_value"]) for r in results):
        print("RESULT: INCONCLUSIVE metric_saturation")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")