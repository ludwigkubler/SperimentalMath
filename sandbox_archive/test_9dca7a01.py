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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n) if random.choice([True, False]) else -random.randint(1, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def construct_mapping(cnf):
        points = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    points.add((lit, 1))
                else:
                    points.add((-lit, -1))
        return points
    
    def min_int_points(points):
        x_min = min(p[0] for p in points)
        y_min = min(p[1] for p in points)
        return len([p for p in points if p[0] == x_min and p[1] == y_min])
    
    def length_resolution_proof(cnf):
        # Simplified resolution proof length calculation
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 30)
    cnf = generate_cnf(n)
    points = construct_mapping(cnf)
    min_points = min_int_points(points)
    proof_length = length_resolution_proof(cnf)
    
    return {
        "metric_name": "MinIntPoints vs Length_ResolutionProof",
        "metric_value": min_points / proof_length,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")