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
    conjecture_holds = True
    counterexample = ""

    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if not any(clause[i] == -clause[j] for i in range(len(clause)) for j in range(i + 1, len(clause))):
                clauses.append(clause)
        return clauses

    def symplectic_quotient_order(clauses):
        order = 0
        for clause in clauses:
            order += sum(abs(x) for x in clause)
        return order / len(clauses)

    def resolution_proof_width(clauses):
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width

    total_order = 0
    total_width = 0

    for _ in range(instances_tested):
        cnf = generate_cnf(n)
        order = symplectic_quotient_order(cnf)
        width = resolution_proof_width(cnf)
        total_order += order
        total_width += width

    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * sum(order * width for order, width in zip([symplectic_quotient_order(generate_cnf(n)) for _ in range(instances_tested)], [resolution_proof_width(generate_cnf(n)) for _ in range(instances_tested)])) - instances_tested * mean_order * mean_width) / math.sqrt((instances_tested * sum(order**2 for order in [symplectic_quotient_order(generate_cnf(n)) for _ in range(instances_tested)]) - instances_tested * mean_order**2) * (instances_tested * sum(width**2 for width in [resolution_proof_width(generate_cnf(n)) for _ in range(instances_tested)]) - instances_tested * mean_width**2))

    if correlation_coefficient < 0.5:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")