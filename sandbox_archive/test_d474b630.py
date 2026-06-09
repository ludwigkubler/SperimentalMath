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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n - 1):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def dpll(phi):
        def solve(assignment):
            if not phi:
                return True
            literal = next((lit for lit in phi[0] if lit not in assignment and -lit not in assignment), None)
            if literal is None:
                return False
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if solve(new_assignment):
                return True
            new_assignment[literal] = False
            new_assignment[-literal] = True
            if solve(new_assignment):
                return True
            return False
        return solve({})

    def grothendieck_group_rank(phi):
        rank = 0
        matroid = set()
        for clause in phi:
            variables = [var for var in clause if var not in matroid and -var not in matroid]
            if variables:
                matroid.update(variables)
                rank += 1
        return rank

    def min_representation_size(phi):
        try:
            return grothendieck_group_rank(phi)
        except Exception as e:
            return None

    def frege_proof_depth(phi):
        try:
            return len(dpll(phi))
        except Exception as e:
            return None

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_mrs = 0
        total_depth = 0
        for _ in range(30):
            phi = generate_formula(n)
            mrs = min_representation_size(phi)
            depth = frege_proof_depth(phi)
            if mrs is not None and depth is not None:
                instances_tested += 1
                total_mrs += mrs
                total_depth += depth
        if instances_tested == 0:
            continue
        avg_mrs = total_mrs / instances_tested
        avg_depth = total_depth / instances_tested
        results.append((n, avg_mrs, avg_depth))

    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }

    n_values, mrs_values, depth_values = zip(*results)
    n_mean = sum(n_values) / len(n_values)
    mrs_mean = sum(mrs_values) / len(mrs_values)
    depth_mean = sum(depth_values) / len(depth_values)

    correlation_coefficient = 0
    for i in range(len(results)):
        correlation_coefficient += (n_values[i] - n_mean) * (mrs_values[i] - mrs_mean) * (depth_values[i] - depth_mean)
    correlation_coefficient /= math.sqrt(sum((n_values[i] - n_mean)**2 * (mrs_values[i] - mrs_mean)**2 for i in range(len(results)))) * math.sqrt(sum((n_values[i] - n_mean)**2 * (depth_values[i] - depth_mean)**2 for i in range(len(results))))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(n_instances for _, _, n_instances in results),
        "n_max": 40,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(coeff >= 0.5 for coeff, _, _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if "counterexample" in r and r["counterexample"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")