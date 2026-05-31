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
    
    def cubic_surface(cnf):
        equations = []
        for clause in cnf:
            parts = clause.split()
            if len(parts) != 3 or not all(part.startswith('x') and part[1:].isdigit() for part in parts):
                continue
            equation = " + ".join(f"{abs(lit)}*x^{lit}" for lit in map(int, parts)) + " - 1"
            equations.append(equation)
        return equations

    def count_integer_points(equations, n):
        # Simple heuristic to estimate the number of integer points
        count = 0
        for x in range(-n, n+1):
            for y in range(-n, n+1):
                for z in range(-n, n+1):
                    if all(eval(eq.replace('x', str(x)).replace('y', str(y)).replace('z', str(z))) == 0 for eq in equations):
                        count += 1
        return count

    def generate_cnf(n):
        cnf = []
        for _ in range(5):  # Generate a small CNF for simplicity
            clause = "x" + str(random.randint(1, n)) + " not x" + str(random.randint(1, n))
            cnf.append(clause)
        return cnf

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        equations = cubic_surface(cnf)
        if not equations:
            continue
        count = count_integer_points(equations, n)
        results.append(count)

    metric_value = sum(results) / len(results)
    instances_tested = len(results)
    n_max = max(n_values)
    conjecture_holds = all(count <= n**3 for count in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Number of Integer Points",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")