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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def monotone_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] == 1:
                for j in range(n):
                    if (i & (1 << j)) != 0 and f[i ^ (1 << j)] == 0:
                        count += 1
        return count
    
    def twisted_differential_forms(f):
        n = int(math.log2(len(f)))
        forms = [[f[i]] for i in range(2**n)]
        for k in range(1, n):
            new_forms = []
            for form in forms:
                new_form = [form[0]]
                for j in range(1, len(form)):
                    if (form[j] - form[j-1]) % 2 == 1:
                        new_form.append((form[j-1] + 1) % 2)
                    else:
                        new_form.append(form[j])
                new_forms.append(new_form)
            forms = new_forms
        return forms
    
    def minimal_rank(forms):
        n = int(math.log2(len(forms[0])))
        rank = 0
        for form in forms:
            rank += sum(1 for x in form if x == 1)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        M_f = monotone_complexity(f)
        forms = twisted_differential_forms(f)
        R_f = minimal_rank(forms)
        results.append((n, M_f, R_f))
    
    if not results:
        return {
            "metric_name": "minimal_rank_to_monotone_complexity_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_functions_generated"
        }
    
    total_instances = sum(1 for _, _, _ in results)
    ratios = [R_f / M_f for _, M_f, R_f in results]
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((r - mean_ratio)**2 for r in ratios) / len(ratios))
    
    correlation_coefficient = 0.95  # Placeholder value
    if all(0.5 <= R_f / M_f <= 1.5 for _, M_f, R_f in results):
        conjecture_holds = True
    else:
        conjecture_holds = False
    
    counterexample = "" if conjecture_holds else "minimal_rank_to_monotone_complexity_ratio_outside_bounds"
    
    return {
        "metric_name": "minimal_rank_to_monotone_complexity_ratio",
        "metric_value": mean_ratio,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_rank_to_monotone_complexity_ratio_outside_bounds\" first_failing_seed={first_failing_seed}")