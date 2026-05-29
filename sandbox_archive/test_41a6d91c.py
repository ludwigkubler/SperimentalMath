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
    
    def generate_cnf(n, m):
        clauses = set()
        for _ in range(m):
            clause = []
            for _ in range(2):  # Each clause has at least 2 literals
                var = random.randint(1, n)
                polarity = random.choice([True, False])
                clause.append((var, polarity))
            clauses.add(tuple(sorted(clause)))
        return clauses

    def resolution_proof_length(clauses):
        stack = list(clauses)
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    clause_i = set(x[0] for x in stack[i])
                    clause_j = set(x[0] for x in stack[j])
                    if len(clause_i & clause_j) == 1:
                        new_clause = [(x[0], not x[1]) for x in stack[i] if x[0] not in clause_j]
                        new_clause.extend([(y[0], not y[1]) for y in stack[j] if y[0] not in clause_i])
                        new_clause = tuple(sorted(new_clause))
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)

    def count_arithmetic_progressions(clauses):
        count = 0
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                clause_i = set(x[0] for x in clauses[i])
                clause_j = set(x[0] for x in clauses[j])
                if len(clause_i & clause_j) == 2:
                    diff = abs(next(iter(clause_i)) - next(iter(clause_j)))
                    if diff > 2:
                        count += 1
        return count

    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    proof_length = resolution_proof_length(cnf)
    ap_count = count_arithmetic_progressions(cnf)

    if ap_count > math.log(proof_length):
        return {
            "metric_name": "arithmetic_progression_count",
            "metric_value": ap_count,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Instance with n={n}, m={m} has {ap_count} arithmetic progressions > α * log({proof_length})"
        }
    else:
        return {
            "metric_name": "arithmetic_progression_count",
            "metric_value": ap_count,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]]
    if not seeds:
        from sympy import primerange
        seeds = list(primerange(2, 100))[:30]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    total_metric_value = sum(result["metric_value"] * result["instances_tested"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 * result["instances_tested"] for result in results) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={n}, m={m} has {ap_count} arithmetic progressions > α * log({proof_length})\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")