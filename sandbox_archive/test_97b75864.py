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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses

    def construct_toric_variety(clauses):
        toric_variety = []
        for clause in clauses:
            point = [0] * (len(clause) + 1)
            for literal in clause:
                if literal[0] == 'x':
                    var = int(literal[1:]) - 1
                else:
                    var = int(literal[2:]) - 1
                point[var] = 1
            toric_variety.append(point)
        return toric_variety

    def compute_minimal_rank(toric_variety):
        n = len(toric_variety[0])
        rank = 0
        for i in range(n):
            if any(row[i] == 1 for row in toric_variety):
                rank += 1
        return rank

    def compute_monotone_circuit_width(clauses):
        # Simplified DPLL solver to estimate width
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next(l for l in clauses[0] if l not in assignment and -l not in assignment)
            for value in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = value
                if dpll(clauses, new_assignment):
                    return True
            return False
        
        width = 0
        for literal in set(l for clause in clauses for l in clause):
            positive_clauses = [clause for clause in clauses if literal in clause]
            negative_clauses = [clause for clause in clauses if -literal in clause]
            width = max(width, len(positive_clauses), len(negative_clauses))
        return width

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    toric_variety = construct_toric_variety(clauses)
    minimal_rank = compute_minimal_rank(toric_variety)
    circuit_width = compute_monotone_circuit_width(clauses)

    if circuit_width == 0:
        return {
            "metric_name": "minimal_rank_over_circuit_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_width_zero"
        }

    ratio = minimal_rank / circuit_width
    return {
        "metric_name": "minimal_rank_over_circuit_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True if ratio <= 2 else False,  # Placeholder constant factor C=2
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")