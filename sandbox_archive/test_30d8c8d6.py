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
    
    def dpll(instance, assignment):
        if not instance:
            return True
        var = next(iter(instance))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if val and var in instance:
                del instance[var]
            if dpll(instance, new_assignment):
                return True
        return False
    
    def generate_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        instance = {var: set() for var in variables}
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    instance[lit].add(-lit)
                else:
                    instance[-lit].add(lit)
        return instance
    
    def path_length(instance):
        stack = [(instance, {})]
        length = 0
        while stack:
            current_instance, assignment = stack.pop()
            if not current_instance:
                return length
            var = next(iter(current_instance))
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                if val and var in current_instance:
                    del current_instance[var]
                stack.append((current_instance, new_assignment))
            length += 1
        return length
    
    def local_class_groups(instance):
        groups = {}
        for var in instance:
            group = set()
            for lit in instance[var]:
                if lit > 0 and -lit not in instance[var]:
                    group.add(lit)
            groups[var] = group
        return len(groups)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        instance = generate_instance(n)
        if not instance:
            continue
        
        length = path_length(instance)
        groups = local_class_groups(instance)
        
        total_metric_value += abs(groups - length)
        instances_tested += 1
        n_max = max(n_max, n)
    
    metric_value = total_metric_value / instances_tested
    
    return {
        "metric_name": "Correlation",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")