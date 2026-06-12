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
    
    def generate_boolean_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return clauses
    
    def construct_quandle(clauses):
        elements = set()
        for clause in clauses:
            for literal in clause:
                elements.add(literal)
        
        quandle = {e: e for e in elements}
        
        def operation(a, b):
            if a == b:
                return a
            elif a in quandle and b in quandle[a]:
                return quandle[b]
            else:
                return None
        
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    quandle[clause[i]] = clause[j]
        
        return quandle
    
    def minimal_quandle_rank(quandle):
        elements = list(quandle.keys())
        n = len(elements)
        if n == 0:
            return 0
        
        rank = 0
        seen = set()
        for current in elements:
            for other in elements:
                if operation(current, other) == other and other not in seen:
                    seen.add(other)
        
        return len(seen)
    
    def clause_tree_depth(clauses):
        depth = 0
        stack = []
        for clause in clauses:
            stack.append((clause, 1))
            while stack:
                current_clause, current_depth = stack.pop()
                if any(lit not in quandle or quandle[lit] == lit for lit in current_clause):
                    depth = max(depth, current_depth)
                else:
                    for lit in current_clause:
                        next_clauses = [c for c in clauses if lit in c]
                        if next_clauses:
                            stack.extend((next_clause, current_depth + 1) for next_clause in next_clauses)
        return depth
    
    n_max = 40
    instances_tested = 30
    qrank_values = []
    ctdepth_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        formula = generate_boolean_formula(n)
        quandle = construct_quandle(formula)
        qrank = minimal_quandle_rank(quandle)
        ctdepth = clause_tree_depth(formula)
        
        qrank_values.append(qrank)
        ctdepth_values.append(ctdepth)
    
    if len(qrank_values) == 0 or len(ctdepth_values) == 0:
        return {
            "metric_name": "qrank_vs_ctdepth",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_formula"
        }
    
    correlation_coefficient = sum((q - q_mean) * (c - c_mean) for q, c in zip(qrank_values, ctdepth_values)) / math.sqrt(sum((q - q_mean)**2 for q in qrank_values) * sum((c - c_mean)**2 for c in ctdepth_values))
    q_mean = sum(qrank_values) / instances_tested
    c_mean = sum(ctdepth_values) / instances_tested
    
    return {
        "metric_name": "qrank_vs_ctdepth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE some_metric_values_are_none")