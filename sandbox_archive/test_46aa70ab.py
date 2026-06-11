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
    
    def generate_boolean_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(instance):
        if not instance:
            return True
        var = instance[0]
        pos_clauses = [cl for cl in instance if var in cl]
        neg_clauses = [cl for cl in instance if -var in cl]
        
        if any(dpll(clause) for clause in pos_clauses):
            return True
        elif all(not dpll(clause) for clause in neg_clauses):
            return False
        else:
            return False
    
    def mld(instance):
        n = len(instance)
        clauses = [set(clause) for clause in instance]
        max_clause_length = max(len(clause) for clause in clauses)
        
        # Simplified version of local induction dimension calculation
        return max_clause_length
    
    results = []
    for n in range(5, 41):
        instances = [generate_boolean_instance(n) for _ in range(30)]
        mld_values = [mld(instance) for instance in instances]
        w_dpll_values = [dpll(instance) for instance in instances]
        
        if not all(w_dpll_values):
            continue
        
        correlation_coefficient = sum((x - sum(mld_values) / len(mld_values)) * (y - sum(w_dpll_values) / len(w_dpll_values)) for x, y in zip(mld_values, w_dpll_values)) / math.sqrt(sum((x - sum(mld_values) / len(mld_values)) ** 2 for x in mld_values) * sum((y - sum(w_dpll_values) / len(w_dpll_values)) ** 2 for y in w_dpll_values))
        
        if correlation_coefficient < 0.8:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": correlation_coefficient,
                "instances_tested": len(instances),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "low_correlation"
            }
        
        results.extend(zip(mld_values, w_dpll_values))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    mld_values, w_dpll_values = zip(*results)
    mean_mld = sum(mld_values) / len(mld_values)
    mean_w_dpll = sum(w_dpll_values) / len(w_dpll_values)
    support_fraction = sum(abs(x - y) <= 3 for x, y in results) / len(results)
    
    return {
        "metric_name": "mld_minus_w_dpll",
        "metric_value": mean_mld - mean_w_dpll,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if 'counterexample' in result)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_data")