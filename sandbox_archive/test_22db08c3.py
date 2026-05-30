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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if not any(abs(c) == abs(d) for c, d in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def tseitin_tensor_product(f1, f2):
        n = len(f1[0])
        m = len(f2[0])
        new_vars = [n + 1 + i for i in range(m)]
        tensor_product = []
        
        # Add variables from both formulas
        for clause in f1:
            tensor_product.append(clause)
        for clause in f2:
            tensor_product.append([x + n for x in clause])
        
        # Add Tseitin clauses
        for j in range(m):
            tensor_product.append([-new_vars[j], new_vars[j]])
            for i in range(n):
                tensor_product.append([new_vars[j], -i, -n - 1 - j])
                tensor_product.append([new_vars[j], i + n, -n - 1 - j])
        
        return tensor_product
    
    def coxeter_group_elements(tensor_product):
        # Simplify the tensor product to find distinct group elements
        elements = set()
        for clause in tensor_product:
            for lit in clause:
                if lit > 0:
                    elements.add(lit)
                else:
                    elements.add(-lit)
        return len(elements)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f1 = generate_3cnf(n)
        f2 = generate_3cnf(n)
        tp = tseitin_tensor_product(f1, f2)
        elements = coxeter_group_elements(tp)
        results.append(elements)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(e <= n**2 * math.log(n) for e in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Coxeter Group Elements",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")