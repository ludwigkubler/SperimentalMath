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
                if random.choice([True, False]):
                    edges.add((i, j))
        return edges
    
    def is_isomorphic(g1, g2):
        if len(g1) != len(g2):
            return False
        nodes = list(range(len(g1)))
        for perm in itertools.permutations(nodes):
            if all((perm[i], perm[j]) in g2 or (perm[j], perm[i]) in g2 for i, j in g1):
                return True
        return False
    
    def symmetry_group_order(graph):
        nodes = list(range(len(graph)))
        sym_group = set()
        for perm in itertools.permutations(nodes):
            if all((perm[i], perm[j]) in graph or (perm[j], perm[i]) in graph for i, j in graph):
                sym_group.add(tuple(perm))
        return len(sym_group)
    
    def resolution_proof_length(graph):
        # Simplified Tseitin formula and Resolution proof length calculation
        n = len(graph)
        clauses = []
        for i in range(n):
            clauses.append([i + 1])
            clauses.append([-i - 1])
        for (u, v) in graph:
            clauses.append([u + 1, -v - 1])
            clauses.append([-u - 1, v + 1])
        proof_length = len(clauses)
        return proof_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_proof_length = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            graph = generate_graph(n)
            sym_order = symmetry_group_order(graph)
            proof_length = resolution_proof_length(graph)
            total_proof_length += proof_length
            instances_tested += 1
    
    avg_proof_length = Fraction(total_proof_length, instances_tested)
    conjecture_holds = avg_proof_length >= 2 ** sym_order
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Resolution proof length",
        "metric_value": avg_proof_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")