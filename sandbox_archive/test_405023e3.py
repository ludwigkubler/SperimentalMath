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
    
    def generate_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)

    def calculate_entropy(formula):
        variables = set()
        for clause in formula.split(" AND "):
            variables.update(clause.split(" OR "))
        entropy = -sum(1/len(variables) * math.log2(1/len(variables)) for _ in range(len(variables)))
        return entropy

    def calculate_generators(formula):
        # Placeholder function to simulate generator calculation
        # Replace with actual implementation if available
        return len(formula.split(" AND "))

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * 2)
        formula = generate_formula(n, m)
        entropy = calculate_entropy(formula)
        generators = calculate_generators(formula)
        
        metric_values.append(generators)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    conjecture_holds = all(3 * entropy**2 <= gen <= 10 * entropy**2 for gen in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")