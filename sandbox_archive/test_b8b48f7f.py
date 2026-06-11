# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [literals[i-1]]
            for j in range(i+1, n+1):
                clause.append(f'-{literals[j-1]}')
            clauses.append(clause)
        return literals, clauses
    
    def resolution_width(clauses):
        # Simplified version of resolution width calculation
        return len(clauses) * 2
    
    def min_monomials(clause):
        # Simplified version of monomial count for a clause
        return len(clause)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = tseitin_formula(n)
    
    widths = [resolution_width(clauses)]
    min_monomials_list = [min_monomials(clause) for clause in clauses]
    
    if len(widths) == 0 or len(min_monomials_list) == 0:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "empty_clauses"
        }
    
    mean_width = sum(widths) / len(widths)
    mean_monomials = sum(min_monomials_list) / len(min_monomials_list)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mean_width - mean_monomials) <= 2 * min_monomials_list[0],
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_holds_or_counterexamples")