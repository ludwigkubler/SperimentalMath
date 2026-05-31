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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        literals = set()
        for clause in cnf:
            literals.update(clause)
        
        literal = next((l for l in literals if l not in assignment and -l not in assignment), None)
        if literal is None:
            return True
        
        def propagate(lit):
            new_assignment = assignment.copy()
            new_assignment[lit] = True
            for clause in cnf:
                if lit in clause:
                    clause.remove(lit)
                elif -lit in clause:
                    clause.remove(-lit)
                if not clause:
                    return False
            return True
        
        def backtrack():
            while literal is not None:
                if propagate(literal):
                    result = dpll(cnf, assignment=new_assignment)
                    if result:
                        return True
                else:
                    del new_assignment[lit]
                    literal = next((l for l in literals if l not in new_assignment and -l not in new_assignment), None)
            return False
        
        return backtrack()
    
    def solve(cnf):
        return dpll(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mli_values = []
    dpll_path_lengths = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * (n - 1) // 2))
            mli_value = len(cnf)  # Simplified local index as number of clauses
            dpll_path_length = solve(cnf)
            
            mli_values.append(mli_value)
            dpll_path_lengths.append(dpll_path_length)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(mli_values, dpll_path_lengths)) / len(mli_values)
    mean_mli = sum(mli_values) / len(mli_values)
    mean_dpll = sum(dpll_path_lengths) / len(dpll_path_lengths)
    
    if correlation_coefficient >= 0.8 and abs(mean_mli - mean_dpll) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_coefficient=<{}> mean_diff=<{}>".format(correlation_coefficient, abs(mean_mli - mean_dpll))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mli_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[results.index(next(r for r in results if not r["conjecture_holds"]))]["counterexample"], first_failing_seed))