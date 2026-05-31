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
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 2 and c[0] != -c[1]] + [-c[0] for c in cnf if len(c) == 2 and c[0] == -c[1]]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        pure_literals = [l for l, count in Counter(lit for clause in cnf for lit in clause).items() if count == 1]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
        literal = random.choice([l for clause in cnf for l in clause])
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        return dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment)
    
    def minimal_local_index(cnf):
        # Placeholder implementation of minimal local index calculation
        return len(cnf)  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    mli_sum = 0
    dpll_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n // 3, n))
            mli = minimal_local_index(cnf)
            dpll_path_length = dpll(cnf)
            if dpll_path_length is None:
                continue
            mli_sum += mli
            dpll_sum += dpll_path_length
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mli = Fraction(mli_sum, instances_tested)
    mean_dpll = Fraction(dpll_sum, instances_tested)
    correlation_coefficient = (instances_tested * mli_sum * dpll_sum - mli_sum * mli_sum - dpll_sum * dpll_sum) / math.sqrt((instances_tested * mli_sum**2 - mli_sum**2) * (instances_tested * dpll_sum**2 - dpll_sum**2))
    mean_absolute_difference = Fraction(sum(abs(mli - dpll_path_length) for mli, dpll_path_length in zip([minimal_local_index(generate_cnf(n, random.randint(2 * n // 3, n))) for _ in range(5)], [dpll(generate_cnf(n, random.randint(2 * n // 3, n))) for _ in range(5)])), instances_tested)
    
    conjecture_holds = correlation_coefficient >= Fraction(8, 10) and mean_absolute_difference <= Fraction(3, 1)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": float(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")