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
    
    def geometric_entropy(n):
        # Simplified version for demonstration purposes
        return n * (math.log(n, 2) + 1)

    def dpll(cnf):
        # Dummy DPLL implementation
        if not cnf:
            return True
        literal = next(iter(cnf))
        pos_cnf = [clauses for clauses in cnf if literal not in clauses]
        neg_cnf = [clauses for clauses in cnf if -literal not in clauses]
        if dpll(pos_cnf):
            return True
        if dpll(neg_cnf):
            return True
        return False

    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf

    n_values = [5, 10, 15, 20, 30, 40]
    results = []

    for n in n_values:
        instances_tested = 0
        total_entropy = 0
        total_length = 0

        while instances_tested < 30:
            cnf = generate_cnf(n, random.randint(1, n))
            entropy = geometric_entropy(n)
            proof_length = len(dpll(cnf))

            if proof_length > 0:
                total_entropy += entropy
                total_length += proof_length
                instances_tested += 1

        mean_entropy = total_entropy / instances_tested
        mean_length = total_length / instances_tested

        results.append({
            "n": n,
            "mean_entropy": mean_entropy,
            "mean_length": mean_length
        })

    metric_value = sum(result["mean_length"] for result in results) / len(results)
    n_max = max(result["n"] for result in results)

    # Check if the data supports the conjecture
    support_fraction = 0.9
    if all(abs(result["mean_length"] - (result["n"] ** 2 * math.log(result["n"], 2))) < result["n"] ** 2 * math.log(result["n"], 2) * 0.1 for result in results):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "geometric_entropy_vs_proof_length"

    return {
        "metric_name": "Proof Length",
        "metric_value": metric_value,
        "instances_tested": 30 * len(n_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"geometric_entropy_vs_proof_length\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")