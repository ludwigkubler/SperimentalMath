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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def convex_hull(points):
        # Implement convex hull algorithm (e.g., Graham's scan)
        pass
    
    def lattice_points_count(convex_hull_points):
        # Count lattice points inside or on the convex hull
        pass
    
    def matrix_representation(f, n):
        # Convert boolean function to a matrix representation
        pass
    
    def rank(matrix):
        # Calculate the rank of the matrix
        pass
    
    total_lattice_points = 0
    total_rank = 0
    instances_tested = 0
    n_max = 5
    
    for n in range(5, 41, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        f = generate_boolean_function(n)
        convex_hull_points = convex_hull(f)
        lattice_points = lattice_points_count(convex_hull_points)
        matrix = matrix_representation(f, n)
        mat_rank = rank(matrix)
        
        total_lattice_points += lattice_points
        total_rank += mat_rank
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    average_lattice_points = total_lattice_points / instances_tested
    average_rank = total_rank / instances_tested
    ratio = average_lattice_points / average_rank
    
    conjecture_holds = ratio <= 2.0  # Example constant k=2 for simplicity
    counterexample = "" if conjecture_holds else f"Ratio {ratio} > 2"
    
    return {
        "metric_name": "Lattice Point Count to Rank Ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds 2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")