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
    
    def generate_polynomial(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        poly = sum(random.choice([1, -1]) * x**random.randint(1, 3) for x in variables)
        return poly

    def polynomial_to_cnf(poly):
        # Convert polynomial to CNF formula (simplified example)
        cnf = []
        for term in poly.split(' '):
            if '+' in term:
                continue
            if '-' in term:
                term = term.replace('-', '+-')
            terms = term.split('+')
            clause = []
            for t in terms:
                if '*' in t:
                    coeff, var = t.split('*')
                    if coeff == '-1':
                        clause.append(f'~{var}')
                    else:
                        clause.append(var)
                elif t.startswith('~'):
                    clause.append(t[1:])
                else:
                    clause.append(t)
            cnf.append(clause)
        return cnf

    def calculate_lid(poly):
        # Simplified example of LID calculation
        return len(poly.split(' '))

    def calculate_sat_complexity(cnf):
        # Simplified example of SAT complexity calculation
        max_clauses = 0
        for clause in cnf:
            if len(clause) > max_clauses:
                max_clauses = len(clause)
        return max_clauses

    n_max = 40
    instances_tested = 30
    metric_values = []

    for _ in range(instances_tested):
        poly = generate_polynomial(random.randint(5, n_max))
        cnf = polynomial_to_cnf(poly)
        lid = calculate_lid(poly)
        sat_complexity = calculate_sat_complexity(cnf)

        metric_values.append(lid - sat_complexity)

    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    conjecture_holds = all(abs(x) <= 3 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "LID - SAT_Complexity",
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")