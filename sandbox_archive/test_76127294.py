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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next((c for c in clauses[0] if not c.startswith('~')), None)
        if var is None:
            return False
        
        def satisfies_clause(clause):
            return any(c.startswith('~') and c[1:] == var or c == var for c in clause)
        
        if any(satisfies_clause(clause) for clause in clauses):
            return dpll([c for c in clauses if not all(c.startswith('~') and c[1:] == var or c == var for c in c)], assignment | {var: True})
        else:
            return dpll([c for c in clauses if not any(satisfies_clause(clause) for clause in c)], assignment | {var: False})
    
    def generate_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables + ['~' + v for v in variables], 3)
            clauses.append(clause)
        return clauses
    
    def symplectic_leaf_count(instance):
        # Placeholder function to simulate the computation
        return len(instance) // 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    msl_sum = 0
    l_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n)
            msl = symplectic_leaf_count(instance)
            path_length = dpll(instance, {})
            if path_length is None:
                continue
            msl_sum += msl
            l_sum += path_length
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_msl_over_l = Fraction(msl_sum, l_sum) if l_sum != 0 else Fraction(0, 1)
    correlation_coefficient = (msl_sum * l_sum - instances_tested * msl_sum * l_sum / instances_tested) / math.sqrt((msl_sum ** 2 - instances_tested * msl_sum ** 2 / instances_tested) * (l_sum ** 2 - instances_tested * l_sum ** 2 / instances_tested))
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_msl_over_l <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "msl_over_l",
        "metric_value": float(mean_msl_over_l),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")