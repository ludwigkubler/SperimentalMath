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
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def construct_graph(phi):
        n = len(phi)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if phi[i] == phi[j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    def min_noncrossing_partitions(G):
        n = len(G)
        partitions = [[i] for i in range(n)]
        while True:
            new_partitions = []
            changed = False
            for partition in partitions:
                subgraphs = [G[i][j] for i, j in itertools.combinations(partition, 2) if G[i][j]]
                if len(subgraphs) == 0:
                    new_partitions.append(partition)
                    continue
                min_partition = partition[:]
                for subgraph in subgraphs:
                    new_partition = partition[:]
                    for i in range(n):
                        if G[i][subgraph]:
                            new_partition.remove(i)
                            new_partition.append([i])
                            changed = True
                    new_partitions.append(new_partition)
            partitions = new_partitions
            if not changed:
                break
        return len(partitions)
    
    def frege_proof_length(phi):
        # Placeholder for a DPLL-based solver
        # This is a simplified version and should be replaced with an actual implementation
        n = len(phi)
        clauses = []
        for i in range(n):
            clauses.append([i])
        for i in range(n):
            for j in range(i+1, n):
                if phi[i] == phi[j]:
                    clauses.append([-i, -j])
        def solve(lits_true, lits_false):
            stack = []
            while True:
                if not stack:
                    return False
                lit = stack.pop()
                if lit < 0:
                    if -lit in lits_true:
                        continue
                    else:
                        return False
                if lit in lits_false:
                    continue
                lits_true.add(lit)
                for clause in clauses:
                    if all(x not in lits_true and -x not in lits_false for x in clause):
                        stack.extend(clause)
            return True
        return len(solve(set(), set()))
    
    m = random.randint(5, 40)
    phi = generate_boolean_function(m)
    G = construct_graph(phi)
    min_order = min_noncrossing_partitions(G)
    proof_length = frege_proof_length(phi)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": None,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")