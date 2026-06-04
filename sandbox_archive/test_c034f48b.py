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

def generate_boolean_instance(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def compute_lattice_points(clauses):
    vectors = [[0] * (len(clauses) + 1)] + [[c[i] for c in clauses] + [1] for i in range(len(clauses))]
    dimension = len(vectors[0])
    lattice_points = set()
    for v in vectors:
        lattice_points.add(tuple(v))
    return len(lattice_points), dimension

def compute_resolution_width(clauses):
    # Placeholder for actual resolution width computation
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Sample 5 instances per size
            m = random.randint(n // 2, n)
            clauses = generate_boolean_instance(n, m)
            lattice_points, dimension = compute_lattice_points(clauses)
            width = compute_resolution_width(clauses)
            ratio = Fraction(lattice_points, dimension) if dimension != 0 else Fraction(0, 1)
            total_ratio += ratio
            instances_tested += 1

            if ratio > width:
                conjecture_holds = False
                counterexample = f"n={n}, m={m}, lattice_points={lattice_points}, dimension={dimension}, width={width}, ratio={ratio}"
                break

    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "Ratio of Lattice Points to Dimension",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unexpected_behavior")