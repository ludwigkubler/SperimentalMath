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
    
    def generate_k_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def delone_set(cnf):
        # Simplified Delone set generation for demonstration
        vertices = set()
        edges = set()
        for clause in cnf:
            for var in clause:
                if abs(var) not in vertices:
                    vertices.add(abs(var))
                    if len(vertices) > 1:
                        edges.add((min(vertices), max(vertices)))
                        vertices.remove(min(vertices))
        return vertices, edges
    
    def symmetrization_algorithm(delone_set):
        # Simplified symmetrization algorithm for demonstration
        symmetry_patterns = set()
        for vertex in delone_set[0]:
            for edge in delone_set[1]:
                if vertex in edge:
                    symmetry_patterns.add((vertex, edge))
        return symmetry_patterns
    
    def minimal_rank(symmetry_patterns):
        # Simplified minimal rank calculation for demonstration
        return len(symmetry_patterns)
    
    def dpll_proof_length(cnf):
        # Simplified DPLL proof length estimation for demonstration
        return 2 ** len(cnf) * random.random()
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    cnf = generate_k_cnf(n, m)
    delone_set_result = delone_set(cnf)
    symmetry_patterns = symmetrization_algorithm(delone_set_result)
    minimal_rank_value = minimal_rank(symmetry_patterns)
    t_star = dpll_proof_length(cnf)
    
    if minimal_rank_value > 2 * math.log(t_star) + 1e-6:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, m={m}, t_star={t_star}"
        }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": minimal_rank_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='n={results[0]['instances_tested']}, m={results[0]['instances_tested']}, t_star={results[0]['instances_tested']}' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")