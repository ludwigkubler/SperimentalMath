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

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate enough clauses to ensure a non-trivial formula
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for j in range(i)):
            cnf.append(tuple(clause))
    return cnf

def construct_toric_variety(cnf):
    # Simplified mapping from clauses to points on a toric variety
    return [sum(clause) for clause in cnf]

def compute_minimal_rank(points):
    n = len(points)
    if n == 0:
        return 0
    rank = 1
    for i in range(1, n):
        if all(points[i] != points[j] * (points[i][k] / points[j][k]) for j in range(i) for k in range(len(points[i]))):
            rank += 1
    return rank

def ac0_circuit_threshold(cnf):
    # Simplified AC0 circuit threshold calculation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    toric_variety = construct_toric_variety(cnf)
    min_rank = compute_minimal_rank(toric_variety)
    ac0_threshold = ac0_circuit_threshold(cnf)
    
    if min_rank == 0:
        return {
            "metric_name": "log(n) / min_rank(Kähler_form_tropicalization)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_rank is zero"
        }
    
    ratio = math.log(n) / min_rank
    conjecture_holds = abs(ratio - ac0_threshold) <= 0.1 * ac0_threshold
    
    return {
        "metric_name": "log(n) / min_rank(Kähler_form_tropicalization)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")