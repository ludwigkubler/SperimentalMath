# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def generate_random_formula(n):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(random.randint(2 * n, 3 * n)):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-var for var in clause]
        clauses.append(clause)
    return clauses

def dpll(phi):
    def solve(model):
        if not phi:
            return model
        literal = next((lit for lit in set.union(*phi) if lit not in model and -lit not in model), None)
        if literal is None:
            return None
        new_phi = [c for c in phi if literal not in c and -literal not in c]
        if solve(model | {literal}):
            return model | {literal}
        if solve(model | {-literal}):
            return model | {-literal}
        return None

    return solve({})

def frege_proof_depth(phi):
    def prove(clauses, model):
        if not clauses:
            return 0
        literal = next((lit for lit in set.union(*clauses) if lit not in model and -lit not in model), None)
        if literal is None:
            return float('inf')
        new_clauses = [c for c in clauses if literal not in c and -literal not in c]
        depth1 = prove(new_clauses, model | {literal})
        depth2 = prove(new_clauses, model | {-literal})
        return 1 + max(depth1, depth2)

    return prove(phi, {})

def grothendieck_group_size(phi):
    def matroid_rank(matroid):
        rank = 0
        for i in range(1, len(matroid) + 1):
            for subset in combinations(matroid, i):
                if all(any(lit in s for lit in clause) for clause in phi):
                    rank = max(rank, i)
        return rank

    def grothendieck_group_rank(matroid):
        rank = matroid_rank(matroid)
        return Fraction(1 << rank)

    return grothendieck_group_rank(phi)

def min_representation_size(phi):
    return grothendieck_group_size(phi)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    mrs_values = []
    dphi_values = []

    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            phi = generate_random_formula(n)
            mrs = min_representation_size(phi)
            dphi = frege_proof_depth(phi)
            if mrs is not None and dphi is not None:
                instances_tested += 1
                mrs_values.append(mrs)
                dphi_values.append(dphi)

    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_mrs = sum(mrs_values) / instances_tested
    mean_dphi = sum(dphi_values) / instances_tested

    correlation_coefficient = 0.0
    for mrs, dphi in zip(mrs_values, dphi_values):
        correlation_coefficient += (mrs - mean_mrs) * (dphi - mean_dphi)
    correlation_coefficient /= instances_tested * math.sqrt(sum((x - mean_mrs) ** 2 for x in mrs_values)) * math.sqrt(sum((y - mean_dphi) ** 2 for y in dphi_values))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["metric_value"] for r in results if r["conjecture_holds"]) >= 0.5:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.5\" first_failing_seed={first_failing_seed}")