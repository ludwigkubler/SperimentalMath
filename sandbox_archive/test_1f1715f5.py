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
    n = 40
    instances_tested = 30
    n_max = 40
    conjecture_holds = False
    counterexample = ""

    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(1, n+1), random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            cnf.append(clause)
        return cnf

    def quadratic_form_rank(cnf):
        # Simplified encoding of quadratic forms
        rank = 0
        for clause in cnf:
            rank += len(set(abs(lit) for lit in clause))
        return rank

    def frege_proof_depth(cnf):
        # Simplified estimation of Frege proof depth
        return len(cnf)

    total_rank = 0
    total_depth = 0

    for _ in range(instances_tested):
        cnf = generate_cnf(n, n)
        rank = quadratic_form_rank(cnf)
        depth = frege_proof_depth(cnf)
        total_rank += rank
        total_depth += depth

    mean_rank = total_rank / instances_tested
    mean_depth = total_depth / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * depth for rank, depth in zip(ranks, depths)) - 
                               sum(ranks) * sum(depths)) / math.sqrt((instances_tested * sum(rank**2 for rank in ranks) - sum(ranks)**2) *
                                                                    (instances_tested * sum(depth**2 for depth in depths) - sum(depths)**2))

    if correlation_coefficient >= 0.8:
        conjecture_holds = True
    elif correlation_coefficient < 0.6:
        counterexample = f"Correlation coefficient {correlation_coefficient} is below threshold"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")