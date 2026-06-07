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
    
    def generate_random_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(random.randint(2 * n, 4 * n)):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(3)]
            clauses.append(clause)
        return clauses

    def diophantine_representation(clauses):
        equations = set()
        for clause in clauses:
            equation = 0
            for literal in clause:
                if literal > 0:
                    equation += literal
                else:
                    equation -= literal
            equations.add(equation)
        return equations

    n_values = [5, 10, 15, 20, 30, 40]
    total_equations = 0
    instances_tested = 0
    max_n = -1
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_random_sat_instance(n)
            equations = diophantine_representation(clauses)
            total_equations += len(equations)
            instances_tested += 1
            if len(equations) > 10:
                return {
                    "metric_name": "num_distinct_diophantine_eqs",
                    "metric_value": len(equations),
                    "instances_tested": instances_tested,
                    "n_max": max_n,
                    "conjecture_holds": False,
                    "counterexample": f"Instance with {len(equations)} equations"
                }
            max_n = max(max_n, n)
    
    mean_equations = total_equations / instances_tested
    return {
        "metric_name": "num_distinct_diophantine_eqs",
        "metric_value": mean_equations,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": mean_equations <= math.sqrt(max_n),
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")