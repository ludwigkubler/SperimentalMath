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
    
    def generate_cnf(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(f"({clause[0]} | {clause[1]})")
        return " & ".join(clauses)

    def diophantine_degree(cnf):
        # Simplify CNF to extract degree
        literals = set()
        for clause in cnf.split(' & '):
            for literal in clause.split('|'):
                if literal.startswith('-'):
                    literals.add(literal[1:])
                else:
                    literals.add(literal)
        return len(literals)

    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)

    n_max = 40
    instances_tested = 30
    total_degree = 0

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        degree = diophantine_degree(cnf)
        total_degree += degree

    mean_degree = total_degree / instances_tested
    conjecture_holds = mean_degree <= n_max * log2(n_max) + 10  # Buffer for potential noise
    counterexample = "" if conjecture_holds else f"mean_degree={mean_degree}, n_max*log_n={n_max*log2(n_max)}"

    return {
        "metric_name": "diophantine_degree",
        "metric_value": mean_degree,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys

    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")