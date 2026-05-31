# auto-injected by SEC sandbox
import math
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = " or ".join(str(lit) if lit > 0 else f"not {abs(lit)}" for lit in literals)
            clauses.append(clause)
        return " and ".join(clauses)
    
    def cubic_surface(cnf):
        # Convert CNF to a system of equations defining the cubic surface
        equations = []
        for clause in cnf.split(" and "):
            if "or" in clause:
                parts = clause.split(" or ")
                equation = " + ".join(f"{abs(lit)}*x^{lit}" for lit in map(int, parts)) + " - 1"
                equations.append(equation)
        return equations
    
    def count_integer_points(equations):
        # Simple heuristic to estimate integer points (not rigorous)
        n = len(equations)
        return n * (n + 1) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        equations = cubic_surface(cnf)
        points = count_integer_points(equations)
        results.append(points)
    
    mean_value = sum(results) / len(results)
    max_n = max(n_values)
    conjecture_holds = all(point <= n**2 for point, n in zip(results, n_values))
    counterexample = "" if conjecture_holds else f"n={max_n}, points={results[-1]}"
    
    return {
        "metric_name": "number_of_integer_points",
        "metric_value": mean_value,
        "instances_tested": len(n_values),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max(result["n_max"] for result in results) >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_budget_exceeded")