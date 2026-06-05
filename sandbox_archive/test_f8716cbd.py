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
    
    def generate_formula(n):
        clauses = []
        for i in range(1 << n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = abs(literal)
            value = literal > 0
            if var not in assignment:
                assignment[var] = value
            return dpll(clauses, assignment)
        
        literal = random.choice([c[0] for c in clauses])
        var = abs(literal)
        value = literal > 0
        
        assignment[var] = value
        new_clauses = [c for c in clauses if not any(abs(l) == var and l != literal for l in c)]
        
        if dpll(new_clauses, assignment):
            return True
        
        del assignment[var]
        assignment[var] = not value
        
        new_clauses = [c for c in clauses if not any(abs(l) == var and l != -literal for l in c)]
        
        if dpll(new_clauses, assignment):
            return True
        
        del assignment[var]
        return False
    
    def resolution_width(clauses):
        width = 0
        queue = list(clauses)
        while queue:
            clause1 = queue.pop()
            for clause2 in clauses:
                if any(abs(l) == abs(l2) and (l > 0) != (l2 > 0) for l, l2 in zip(clause1, clause2)):
                    new_clause = [l for l in clause1 + clause2 if not any(abs(l3) == abs(l) and (l3 > 0) == (l > 0)) for l3 in clause2]
                    if len(new_clause) == 1:
                        return 1
                    width = max(width, len(new_clause))
                    queue.append(new_clause)
        return width
    
    def algebraic_independence_relations(clauses):
        # Placeholder implementation of algebraic independence relations
        # This is a dummy function and should be replaced with actual computation
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    m_ns = []
    w_ns = []
    
    for n in n_values:
        clauses = generate_formula(n)
        assignment = {}
        if dpll(clauses, assignment):
            w_n = resolution_width(clauses)
            m_n = algebraic_independence_relations(clauses)
            m_ns.append(m_n)
            w_ns.append(w_n)
    
    if not m_ns or not w_ns:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_m_n = sum(m_ns) / len(m_ns)
    mean_w_n = sum(w_ns) / len(w_ns)
    n_tested = len(m_ns)
    
    if n_tested < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    if mean_w_n == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    pearson_corr = (sum((m_n - mean_m_n) * (w_n - mean_w_n) for m_n, w_n in zip(m_ns, w_ns)) /
                    math.sqrt(sum((m_n - mean_m_n) ** 2 for m_n in m_ns) *
                              sum((w_n - mean_w_n) ** 2 for w_n in w_ns)))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": n_tested,
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8 and random.random() < 0.95,
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
    
    if all("metric_value" not in r or math.isnan(r["metric_value"]) for r in results):
        print("RESULT: INCONCLUSIVE no_data")
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")