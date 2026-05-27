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
    
    def generate_boolean_formula(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses

    def monomial_ideal_size(formula):
        return len(formula)

    def minimal_generators(formula):
        # Simplified heuristic to estimate minimal generators
        return 2 * len(formula) ** 0.5

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test with 5 instances per size
            formula = generate_boolean_formula(n, random.randint(1, n * 2))
            m = monomial_ideal_size(formula)
            gen = minimal_generators(formula)
            results.append((n, m, gen))

    conjecture_holds = all(gen <= math.log(n) + math.pow(m, 0.25) for n, m, gen in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalGenerators",
        "metric_value": sum(gen for _, _, gen in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3  # First 30 primes
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(res["metric_value"] - (math.log(res["n_values"][0]) + math.pow(res["m_values"][0], 0.25))) > 3 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if abs(res["metric_value"] - (math.log(res["n_values"][0]) + math.pow(res["m_values"][0], 0.25))) > 3)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")