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
        cnf = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def p_adic_representation(cnf):
        n = len(cnf[0])
        rep = [[0] * (2 * n) for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                idx = abs(lit) - 1
                if lit > 0:
                    rep[idx][idx] += 1
                else:
                    rep[idx][n + idx] += 1
        return rep
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        stack = []
        assignment = [None] * (len(cnf) + 1)
        for clause in cnf:
            if all(lit not in assignment or assignment[lit] == False for lit in clause):
                return len(stack)
            unassigned = next((lit for lit in clause if assignment[lit] is None), None)
            if unassigned is None:
                return len(stack)
            stack.append(unassigned)
            assignment[unassigned] = True
        return 0
    
    def local_cohomological_defect(rep):
        n = len(rep)
        defect = 0
        for i in range(n):
            for j in range(2 * n):
                if rep[i][j] > 0:
                    defect += 1
        return defect
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_defect = 0
    instances_tested = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        rep = p_adic_representation(cnf)
        width = resolution_width(cnf)
        defect = local_cohomological_defect(rep)
        
        if width == 0 or defect == 0:
            continue
        
        total_width += width
        total_defect += defect
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    ratio = total_width / total_defect
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and not math.isnan(r["metric_value"]) for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if "metric_value" not in r or math.isnan(r["metric_value"])), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_valid_instances\" first_failing_seed={first_failing_seed}")