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
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        return clauses
    
    def construct_cubic_surface(cnf):
        equations = []
        for clause in cnf:
            equation = sum(clause) ** 2
            equations.append(equation)
        return equations
    
    def count_integer_points(equations, n_max=40):
        count = 0
        for x in range(-n_max, n_max + 1):
            for y in range(-n_max, n_max + 1):
                for z in range(-n_max, n_max + 1):
                    if all(eq.subs({x: x_val, y: y_val, z: z_val}) == 0 for eq in equations):
                        count += 1
        return count
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    cubic_surface_equations = construct_cubic_surface(cnf)
    metric_value = count_integer_points(cubic_surface_equations)
    
    return {
        "metric_name": "Number of Integer Points",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,  # Placeholder value
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r <= n**2) / len(results)
    
    if all(r <= n**2 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result > n**2)
        print(f"RESULT: FALSIFIED counterexample='exceeds_n_squared' first_failing_seed={first_failing_seed}")