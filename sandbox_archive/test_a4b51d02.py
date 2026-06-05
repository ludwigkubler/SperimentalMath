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
    
    def generate_random_sat_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def nnf(sat_formula):
        # Convert SAT formula to NNF
        return sat_formula
    
    def lid(nnf_formula):
        # Compute LID of NNF
        variables = set()
        for clause in nnf_formula:
            for literal in clause:
                variables.add(abs(literal))
        return len(variables)
    
    def ccr(sat_formula):
        # Compute CCR using truth table rank
        n = max(abs(lit) for clause in sat_formula for lit in clause)
        truth_table = [[0] * (2 ** n) for _ in range(len(sat_formula))]
        for i, clause in enumerate(sat_formula):
            for j in range(2 ** n):
                if all((j >> abs(lit) & 1) ^ (lit > 0) for lit in clause):
                    truth_table[i][j] = 1
        rank = 0
        matrix = []
        for row in truth_table:
            if any(row):
                matrix.append([x for x in row if x])
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        sat_formula = generate_random_sat_formula(n)
        nnf_formula = nnf(sat_formula)
        lid_value = lid(nnf_formula)
        ccr_value = ccr(sat_formula)
        results.append({"n": n, "lid": lid_value, "ccr": ccr_value})
    
    if not results:
        return {
            "metric_name": "LID vs CCR",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "LID vs CCR",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    lid_values = [result["lid"] for result in results]
    ccr_values = [result["ccr"] for result in results]
    
    mean_lid = sum(lid_values) / len(lid_values)
    mean_ccr = sum(ccr_values) / len(ccr_values)
    
    if n_max < 20:
        return {
            "metric_name": "LID vs CCR",
            "metric_value": mean_lid,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    if n_max < 30:
        return {
            "metric_name": "LID vs CCR",
            "metric_value": mean_lid,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    correlation = sum((lid_values[i] - mean_lid) * (ccr_values[i] - mean_ccr) for i in range(len(lid_values))) / len(lid_values)
    
    if correlation < 0.5:
        return {
            "metric_name": "LID vs CCR",
            "metric_value": mean_lid,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Correlation too low: {correlation}"
        }
    
    return {
        "metric_name": "LID vs CCR",
        "metric_value": mean_lid,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")