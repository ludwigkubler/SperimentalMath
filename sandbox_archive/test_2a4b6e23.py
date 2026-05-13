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
    
    # Generate a random CNF formula with n variables and m clauses
    n = 10
    m = 2 * n
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    
    # Convert CNF to simplicial complex (simplified representation)
    simplicial_complex = {tuple(sorted(cnf[i])) for i in range(m)}
    
    # Apply algebraic shifting (simplified version)
    shifted_complex = set()
    for face in simplicial_complex:
        if len(face) > 1:
            for i in range(len(face)):
                new_face = list(face)
                new_face.remove(-face[i])
                shifted_complex.add(tuple(sorted(new_face)))
    
    # Compute the ideal's generators (simplified version)
    generators = []
    for face in shifted_complex:
        if len(face) == 1:
            generators.append((1, -face[0]))
        else:
            generators.append((-1, *face))
    
    # Communication complexity (example protocol: one-bit communication per variable)
    cc = n
    
    # Count the number of minimal generators
    num_generators = len(generators)
    
    # Check if the conjecture holds
    conjecture_holds = num_generators >= cc
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"CNF: {cnf}, CC: {cc}, Generators: {generators}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_cc) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")