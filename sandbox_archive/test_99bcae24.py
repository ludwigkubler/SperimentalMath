# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def map_clauses_to_monomials(edges, d):
        monomials = set()
        for edge in edges:
            for clause in combinations(range(len(edge)), d):
                monomial = tuple(sorted(clause))
                monomials.add(monomial)
        return monomials
    
    def compute_newton_polytope_volume(monomials):
        n = len(monomials)
        vertices = []
        for monomial in monomials:
            vertex = [0] * (n + 1)
            for i, m in enumerate(monomial):
                vertex[m] += 1
            vertices.append(vertex)
        
        def determinant(matrix):
            if len(matrix) == 2:
                return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            det = 0
            for j in range(len(matrix)):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
            return det
        
        return abs(determinant(vertices))
    
    def compute_sos_degree(monomials):
        degree = 0
        for monomial in monomials:
            degree = max(degree, sum(monomial))
        return degree
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    d_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    volumes = []
    for d in d_values:
        monomials = map_clauses_to_monomials(edges, d)
        volume = compute_newton_polytope_volume(monomials)
        volumes.append(volume)
    
    if len(volumes) < len(d_values):
        return {
            "metric_name": "Volume",
            "metric_value": None,
            "instances_tested": len(volumes),
            "conjecture_holds": False,
            "counterexample": "Insufficient data"
        }
    
    d_values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected_volumes = [volumes[0] / (d ** 2) for d in d_values]
    
    supports_conjecture = all(abs(v - e) < 1e-6 for v, e in zip(volumes, expected_volumes))
    
    return {
        "metric_name": "Volume",
        "metric_value": volumes[0],
        "instances_tested": len(volumes),
        "conjecture_holds": supports_conjecture,
        "counterexample": "" if supports_conjecture else f"Volumes: {volumes}, Expected: {expected_volumes}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_volume = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_volume = math.sqrt(sum((r["metric_value"] - mean_volume) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_volume} std={std_volume} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")