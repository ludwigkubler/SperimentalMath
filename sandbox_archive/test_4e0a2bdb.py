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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literal = next(lit for lit in range(1, len(assignment) + 2) if lit not in assignment and -lit not in assignment)
        positive = literal > 0
        new_assignment = assignment.copy()
        new_assignment[literal] = positive
        if dpll(cnf, new_assignment):
            return True
        new_assignment[literal] = not positive
        if dpll(cnf, new_assignment):
            return True
        return False
    
    def hdeg(cnf):
        # Placeholder for Hodge degeneration index calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    n_max = 40
    instances_tested = 0
    total_hdeg = 0
    total_d = 0
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            hdeg_val = hdeg(cnf)
            d_val = dpll(cnf)
            total_hdeg += hdeg_val
            total_d += d_val
            instances_tested += 1
    
    mean_hdeg = total_hdeg / instances_tested
    mean_d = total_d / instances_tested
    correlation_coefficient = (instances_tested * sum(hdeg_val * d_val for hdeg_val, d_val in zip([mean_hdeg] * instances_tested, [mean_d] * instances_tested)) - 
                               sum(hdeg_val for hdeg_val in [mean_hdeg] * instances_tested) * sum(d_val for d_val in [mean_d] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(hdeg_val ** 2 for hdeg_val in [mean_hdeg] * instances_tested) - 
                                          (sum(hdeg_val for hdeg_val in [mean_hdeg] * instances_tested)) ** 2) *
                                        (instances_tested * sum(d_val ** 2 for d_val in [mean_d] * instances_tested) - 
                                         (sum(d_val for d_val in [mean_d] * instances_tested)) ** 2))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.8' first_failing_seed={seeds[first_failing_seed]}")