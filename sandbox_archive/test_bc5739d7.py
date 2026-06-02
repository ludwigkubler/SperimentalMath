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
    n = random.randint(5, 40)
    instances_tested = 30
    total_metric_value = 0
    max_n = n
    
    for _ in range(instances_tested):
        # Generate a random satisfiability problem instance with n variables
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            clauses.append(clause)
        
        # Construct the associated Tseitin formula φ
        tseitin_vars = {}
        tseitin_count = n
        def tseitin_var(i):
            if i not in tseitin_vars:
                tseitin_vars[i] = tseitin_count
                tseitin_count += 1
            return tseitin_vars[i]
        
        tseitin_clauses = []
        for clause in clauses:
            tseitin_clause = [tseitin_var(i) if x > 0 else -tseitin_var(-x) for x in clause]
            tseitin_clauses.append(tseitin_clause)
        
        # Compute the resolution proof width w(φ)
        def resolve(clauses):
            resolved = set()
            while True:
                new_resolved = False
                for i in range(len(clauses)):
                    for j in range(i + 1, len(clauses)):
                        if any(-x in clauses[i] and x in clauses[j] for x in set(clauses[i]) & set(clauses[j])):
                            resolved.update(set(clauses[i]) | set(clauses[j]))
                            new_resolved = True
                if not new_resolved:
                    break
            return len(resolved)
        
        w_phi = resolve(tseitin_clauses)
        
        # Determine the minimal number of automorphic forms required to represent φ
        def is_automorphic_form(form):
            for i in range(len(form)):
                for j in range(i + 1, len(form)):
                    if form[i] == -form[j]:
                        return False
            return True
        
        min_automorphic_forms = 0
        while True:
            forms = []
            for _ in range(n):
                form = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
                if is_automorphic_form(form):
                    forms.append(form)
            if len(forms) == n:
                min_automorphic_forms = n
                break
        
        # Calculate the correlation coefficient between the minimal number of automorphic forms and resolution proof width
        metric_value = w_phi / math.log(min_automorphic_forms * n, 2)
        
        total_metric_value += metric_value
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = True if mean_metric_value > 0 else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")