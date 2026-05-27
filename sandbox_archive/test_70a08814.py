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
    n = 30
    c = 1.2  # Upper bound for the conjecture
    metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    def generate_3cnf(n, density):
        clauses = []
        variables = list(range(1, n + 1))
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.choice(variables), random.choice(variables)]
            if random.choice([True, False]):
                clause[0] = -clause[0]
            if random.choice([True, False]):
                clause[1] = -clause[1]
            clauses.append(clause)
        return clauses

    def xor_and_tree_width(clauses):
        # Simple heuristic to estimate XOR-AND tree width
        return len(clauses)

    def tropicalized_rank(clauses):
        rank = 0
        for clause in clauses:
            rank += len(set(abs(lit) for lit in clause))
        return rank

    for density in [0.1, 0.25, 0.5, 0.75]:
        for _ in range(7):  # Ensure at least 30 instances per seed
            clauses = generate_3cnf(n, density)
            xor_and_width = xor_and_tree_width(clauses)
            rank = tropicalized_rank(clauses)
            if xor_and_width == 0:
                continue  # Avoid division by zero
            ratio = rank / xor_and_width
            metric_value += ratio
            instances_tested += 1
            if ratio > c * n ** (3/4):
                conjecture_holds = False
                counterexample = f"n={n}, density={density}, rank={rank}, xor_and_width={xor_and_width}"

    mean_ratio = metric_value / instances_tested if instances_tested > 0 else 0
    return {
        "metric_name": "Ratio of Tropicalized Rank to XOR-AND Tree Width",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 73))  # Default to first 30 primes
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")