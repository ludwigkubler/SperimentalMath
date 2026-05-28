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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            else:
                clause = {x: 1 for x in clause}
            clauses.append(clause)
        return clauses

    def resolution_proof_width(cnf):
        clauses = cnf.copy()
        while True:
            new_clauses = []
            added_clause = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if -clauses[i].intersection(clauses[j]):
                        new_clause = {x: -1 for x in clauses[i] if x not in clauses[j]}
                        new_clause.update({x: -1 for x in clauses[j] if x not in clauses[i]})
                        new_clauses.append(new_clause)
                        added_clause = True
            if not added_clause:
                break
            clauses.extend(new_clauses)
        return len(clauses)

    def arithmetic_genus(cnf):
        n = len(cnf[0])
        genus = 0
        for clause in cnf:
            if any(x < 0 for x in clause.values()):
                genus += 1
        return genus

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf_formula = generate_cnf(n)
    
    g_F = arithmetic_genus(cnf_formula)
    ω_F = resolution_proof_width(cnf_formula)
    
    return {
        "metric_name": "arithmetic genus vs resolution proof width",
        "metric_value": abs(g_F - ω_F),
        "instances_tested": 1,
        "conjecture_holds": g_F <= 10 * ω_F,
        "counterexample": "" if g_F <= 10 * ω_F else f"Arithmetic genus {g_F} > 10 * resolution proof width {ω_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Arithmetic genus > 10 * resolution proof width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")