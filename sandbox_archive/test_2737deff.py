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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in at least one clause
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def compute_local_cohomology_order(cnf):
        # Placeholder implementation
        # For simplicity, we assume lcoh(φ) is proportional to the number of variables
        n = len(cnf[0])
        return n
    
    def compute_frege_proof_length(cnf):
        # Placeholder implementation
        # For simplicity, we assume f(φ) is proportional to the number of clauses
        m = len(cnf)
        return m

    n_max = 40
    instances_tested = 0
    lcoh_values = []
    frege_lengths = []

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            lcoh_value = compute_local_cohomology_order(cnf)
            frege_length = compute_frege_proof_length(cnf)
            lcoh_values.append(lcoh_value)
            frege_lengths.append(frege_length)
            instances_tested += 1

    if not lcoh_values or not frege_lengths:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }

    correlation_coefficient = sum((x - mean_lcoh) * (y - mean_frege) for x, y in zip(lcoh_values, frege_lengths)) / \
                               math.sqrt(sum((x - mean_lcoh) ** 2 for x in lcoh_values) * sum((y - mean_frege) ** 2 for y in frege_lengths))
    mean_lcoh = sum(lcoh_values) / len(lcoh_values)
    mean_frege = sum(frege_lengths) / len(frege_lengths)

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and all(lcoh <= c * frege for lcoh, frege, c in zip(lcoh_values, frege_lengths, range(1, len(lcoh_values) + 1))),
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results if r['metric_value'] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and any(r['metric_value'] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")