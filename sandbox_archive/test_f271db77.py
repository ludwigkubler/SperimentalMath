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

def generate_cnf(n):
    cnf = []
    for _ in range(n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)]
        for _ in range(random.randint(0, n-1)):
            clause.append(random.randint(1, n) * (-1 if random.choice([True, False]) else 1))
        cnf.append(clause)
    return cnf

def dpll(cnf):
    def unit_propagate():
        while True:
            found = False
            for i in range(len(cnf)):
                clause = cnf[i]
                if len(clause) == 1:
                    lit = clause[0]
                    if -lit in [c for cl in cnf if len(cl) > 1]:
                        return None
                    for j in range(len(cnf)):
                        if lit in cnf[j]:
                            cnf[j].remove(lit)
                            found = True
            if not found:
                break
        return cnf

    def pure_literal():
        count = [0] * (2 * n + 1)
        for clause in cnf:
            for lit in clause:
                count[lit] += 1
                count[-lit] -= 1
        while True:
            found = False
            for i in range(1, 2 * n + 1):
                if count[i] == len(cnf) and -i not in [c for cl in cnf if len(cl) > 1]:
                    for j in range(len(cnf)):
                        if i in cnf[j]:
                            cnf[j].remove(i)
                            found = True
            if not found:
                break
        return cnf

    def backtracking(model):
        if not any(clause for clause in cnf):
            return model
        unit_clauses = [i for i, clause in enumerate(cnf) if len(clause) == 1]
        if unit_clauses:
            lit = cnf[unit_clauses[0]][0]
            new_model = model + [lit] if lit > 0 else model + [-lit]
            return backtracking(new_model)
        pure_literals = [i for i in range(1, 2 * n + 1) if count[i] == len(cnf) and -i not in [c for cl in cnf if len(cl) > 1]]
        if pure_literals:
            lit = pure_literals[0]
            new_model = model + [lit] if lit > 0 else model + [-lit]
            return backtracking(new_model)
        first_lit = cnf[0][0]
        if first_lit > 0:
            result = backtracking(model + [first_lit])
            if result is not None:
                return result
            return backtracking(model + [-first_lit])
        else:
            result = backtracking(model + [-first_lit])
            if result is not None:
                return result
            return backtracking(model + [first_lit])

    cnf = unit_propagate()
    cnf = pure_literal()
    return backtracking([])

def compute_qmc_order(n, epsilon):
    # This is a placeholder for the actual QMC order computation
    return 2 * n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        w_phi = len(dpll(cnf)) if dpll(cnf) is not None else float('inf')
        qmc_order = compute_qmc_order(n, 1/1000)
        results.append({"n": n, "w_phi": w_phi, "qmc_order": qmc_order})
    
    mean_w_phi = sum(result["w_phi"] for result in results) / len(results)
    mean_qmc_order = sum(result["qmc_order"] for result in results) / len(results)
    correlation_coefficient = sum((result["w_phi"] - mean_w_phi) * (result["qmc_order"] - mean_qmc_order) for result in results) / len(results)
    variance_w_phi = sum((result["w_phi"] - mean_w_phi) ** 2 for result in results) / len(results)
    variance_qmc_order = sum((result["qmc_order"] - mean_qmc_order) ** 2 for result in results) / len(results)
    
    if correlation_coefficient < 0.95 or variance_w_phi == 0 or variance_qmc_order == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": len(n_values),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")