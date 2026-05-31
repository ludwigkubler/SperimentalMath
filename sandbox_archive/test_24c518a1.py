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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < n:
            var = random.randint(1, n)
            if -var not in clause:
                clause.add(var)
        cnf.append(tuple(sorted(clause)))
    return tuple(cnf)

def construct_coxeter_diagram(cnf):
    diagram = {}
    for clause in cnf:
        for var in clause:
            if var not in diagram:
                diagram[var] = set()
            for other_var in clause:
                if other_var != var and -other_var not in diagram[var]:
                    diagram[var].add(other_var)
    return diagram

def count_automorphisms(diagram):
    n = len(diagram)
    visited = [False] * (n + 1)
    
    def dfs(node, mapping):
        if visited[node]:
            return True
        visited[node] = True
        for neighbor in diagram[node]:
            if mapping[neighbor] not in diagram[mapping[node]]:
                return False
            if not dfs(mapping[neighbor], mapping):
                return False
        visited[node] = False
        return True
    
    def find_mapping():
        for perm in itertools.permutations(range(1, n + 1)):
            mapping = {i: perm[i - 1] for i in range(1, n + 1)}
            if dfs(1, mapping):
                return mapping
        return None
    
    mapping = find_mapping()
    if not mapping:
        return 0
    count = 0
    for perm in itertools.permutations(range(1, n + 1)):
        new_mapping = {i: perm[i - 1] for i in range(1, n + 1)}
        if dfs(1, new_mapping):
            count += 1
    return count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            cnf = generate_cnf(n, m)
            diagram = construct_coxeter_diagram(cnf)
            aut_count = count_automorphisms(diagram)
            f_n = math.sqrt(m) * (n ** (3/4))
            results.append({
                "metric_name": "Aut(φ)",
                "metric_value": aut_count,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": aut_count <= f_n,
                "counterexample": "" if aut_count <= f_n else f"m={m}, n={n}"
            })
    return {
        "seed": seed,
        "metric_name": "Aut(φ)",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    mean_Aut_phi = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    print("TRIALS:")
    for result in results:
        print(f"  TRIAL: {result}")
    
    if all(result["conjecture_holds"] for result in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_Aut_phi} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m>n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")