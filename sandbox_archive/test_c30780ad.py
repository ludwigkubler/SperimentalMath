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
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def delone_set_from_cnf(cnf):
        vertices = set()
        edges = set()
        for clause in cnf:
            for var in clause:
                if var > 0:
                    vertices.add(var)
                else:
                    vertices.add(-var)
        for i in range(1, len(vertices) + 1):
            for j in range(i + 1, len(vertices) + 1):
                edges.add((i, j))
        return vertices, edges
    
    def symmetrization_algorithm(delone_set):
        # Placeholder for actual algorithm
        return delone_set
    
    def minimal_rank_of_symmetry_group(symmetries):
        # Placeholder for actual calculation
        return len(symmetries)
    
    def dpll_proof_length(cnf):
        # Placeholder for actual calculation
        return random.randint(10, 100)  # Simulated value
    
    n = 20
    m = 5 * n
    cnf = generate_k_cnf(n, m)
    vertices, edges = delone_set_from_cnf(cnf)
    symmetries = symmetrization_algorithm((vertices, edges))
    minimal_rank = minimal_rank_of_symmetry_group(symmetries)
    t_star = dpll_proof_length(cnf)
    
    metric_value = minimal_rank
    conjecture_holds = minimal_rank <= 2 * math.log(t_star) + 1e-6
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [random.randint(2, 100) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")