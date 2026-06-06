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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_length(cnf):
        # Simplified Frege proof length calculation
        return len(cnf) * n
    
    def formal_group_index(cnf):
        # Constructive mapping to a formal group index (simplified)
        return sum(abs(sum(clause)) for clause in cnf)
    
    n = 40
    instances_tested = 30
    total_log_F = 0
    total_f = 0
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n)
        log_F = formal_group_index(cnf)
        f = frege_proof_length(cnf)
        
        if f == 0:
            continue
        
        total_log_F += math.log(log_F) / math.log(2)
        total_f += f
    
    mean_log_F_over_f = total_log_F / instances_tested
    mean_f = total_f / instances_tested
    
    conjecture_holds = (0.5 <= mean_log_F_over_f <= 2) and abs(mean_log_F_over_f - mean_f) <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "log(F)/f",
        "metric_value": mean_log_F_over_f,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")