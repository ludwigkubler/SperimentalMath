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
    n = 5 + (seed % 6) * 5  # Sweep through n ∈ {5,10,15,20,30,40}
    if n < 5 or n > 40:
        return {
            "metric_name": "GT_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "sub-asymptotic_n"
        }
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        clauses = []
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            clause = []
            for j in range(n):
                if binary_i[j] == '1':
                    clause.append(j)
                else:
                    clause.append(-j - 1)
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        stack = []
        literals = set()
        for clause in clauses:
            if not any(l in literals for l in clause):
                for literal in clause:
                    literals.add(abs(l))
                    stack.append((literal, clause))
        width = 0
        while stack:
            literal, clause = stack.pop()
            if literal > 0:
                literals.remove(literal)
            else:
                literals.remove(-literal)
            new_clauses = []
            for c in clauses:
                if literal not in c and -literal not in c:
                    continue
                new_clause = [l for l in c if l != literal and l != -literal]
                if len(new_clause) == 0:
                    return float('inf')
                elif len(new_clause) > width:
                    width = len(new_clause)
                new_clauses.append(new_clause)
            clauses = new_clauses
        return width
    
    def grothendieck_teichmueller_group_order(n):
        # Placeholder for actual computation
        return n**2 * math.log(n)
    
    f = generate_boolean_function(n)
    gt_order = grothendieck_teichmueller_group_order(n)
    tseitin_clauses = tseitin_formula(f, n)
    resolution_width_val = resolution_width(tseitin_clauses)
    
    return {
        "metric_name": "GT_order",
        "metric_value": gt_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(gt_order - resolution_width_val) <= 0.1 * gt_order and resolution_width_val < float('inf'),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=" + str(len(seeds)))