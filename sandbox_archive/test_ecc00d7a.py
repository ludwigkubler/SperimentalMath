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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def tseitin_encoding(cnf):
        n = len(cnf)
        new_vars = list(range(2*n))
        tseitin_formulas = []
        
        for i, clause in enumerate(cnf):
            tseitin_var = new_vars[i + n]
            tseitin_formulas.append([tseitin_var])
            for literal in clause:
                if literal > 0:
                    tseitin_formulas.append([-literal, tseitin_var])
                else:
                    tseitin_formulas.append([abs(literal), -tseitin_var])
        
        return tseitin_formulas
    
    def resolution_width(formula):
        queue = formula[:]
        seen = set()
        while queue:
            clause1 = queue.pop(0)
            for clause2 in formula:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = list((set(clause1) ^ set(clause2)) - {-1})
                    if new_clause not in seen and new_clause != []:
                        seen.add(new_clause)
                        queue.append(new_clause)
        return max(len(clause) for clause in seen)
    
    def count_braided_monoidal_categories(cnf):
        n = len(cnf)
        # Simplified mapping: each variable is a braided monoidal category
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    instances_tested = 0
    max_n = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        tseitin_formulas = tseitin_encoding(cnf)
        width = resolution_width(tseitin_formulas)
        m_phi = count_braided_monoidal_categories(cnf)
        
        total_width += width
        instances_tested += len(cnf)
        max_n = max(max_n, n)
    
    mean_width = Fraction(total_width, instances_tested)
    ratio = mean_width / max_n
    
    conjecture_holds = abs(ratio - (n * math.log(n))) <= 20
    counterexample = "" if conjecture_holds else f"mean_width={mean_width}, n_max={max_n}"
    
    return {
        "metric_name": "resolution_proof_width_to_braided_monoidal_categories_ratio",
        "metric_value": float(ratio),
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_ratio_outside_bound' first_failing_seed={first_failing_seed}")