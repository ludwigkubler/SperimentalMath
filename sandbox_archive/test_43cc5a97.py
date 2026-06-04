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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def polynomial_from_clauses(clauses):
        n = len(clauses[0])
        poly = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            monomial = [1]
            for lit in clause:
                if lit > 0:
                    monomial.append(lit)
                else:
                    monomial.append(-lit)
            poly[monomial[-2]][monomial[-1]] += 1
        return poly
    
    def min_order_invariants(poly):
        n = len(poly) - 1
        order = 0
        for i in range(n + 1):
            for j in range(i + 1, n + 1):
                if poly[i][j] != 0:
                    order += abs(j - i)
        return order
    
    def clause_set_simplicity(clauses):
        return sum(len(clause) for clause in clauses)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            poly = polynomial_from_clauses(cnf)
            order = min_order_invariants(poly)
            simplicity = clause_set_simplicity(cnf)
            results.append((n, order, simplicity))
    
    if not results:
        return {
            "metric_name": "minimal_order",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_order = sum(order for _, order, _ in results)
    mean_order = Fraction(total_order, len(results))
    conjecture_holds = all(abs(order - n**2) <= 3 for n, order, _ in results)
    counterexample = "" if conjecture_holds else "order does not match O(n^2)"
    
    return {
        "metric_name": "minimal_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        total_order = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
        mean_order = Fraction(total_order, len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_order} std=NA support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] and result["counterexample"] for result in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient support")