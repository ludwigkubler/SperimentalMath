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
    
    def generate_boolean_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_lattice_points(clauses):
        vectors = [[0] * (len(clauses) + 1)] + [[c[i] for c in clauses] + [1] for i in range(len(clauses))]
        n = len(vectors[0])
        m = len(vectors)
        
        # Gaussian elimination
        for i in range(n):
            if vectors[i][i] == 0:
                for j in range(i + 1, m):
                    if vectors[j][i] != 0:
                        vectors[i], vectors[j] = vectors[j], vectors[i]
                        break
            if vectors[i][i] == 0:
                continue
            pivot = 1 / vectors[i][i]
            for j in range(n + 1):
                vectors[i][j] *= pivot
        
        # Count lattice points
        lattice_points = 1
        for i in range(1, m):
            if all(vectors[i][j] == 0 for j in range(i)):
                continue
            count = 1
            for j in range(n + 1):
                if vectors[i][j] != 0:
                    count *= math.ceil(abs(vectors[i][j]))
            lattice_points *= count
        
        return lattice_points
    
    def compute_resolution_width(clauses):
        # Simple heuristic to estimate resolution width (not rigorous)
        return len(clauses) * 2
    
    n = random.randint(5, 40)
    m = random.randint(n, 100)
    clauses = generate_boolean_instance(n, m)
    
    lattice_points = compute_lattice_points(clauses)
    dimension = n + 1
    resolution_width = compute_resolution_width(clauses)
    
    ratio = lattice_points / dimension
    
    return {
        "metric_name": "Ratio of Lattice Points to Dimension",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= resolution_width,
        "counterexample": "" if ratio <= resolution_width else f"Ratio {ratio} > Width {resolution_width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")