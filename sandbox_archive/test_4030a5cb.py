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
        literals = [i for i in range(1, n+1)] + [-i for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(literals, 2)
            clauses.append(clause)
        return clauses
    
    def mrd(clauses):
        variables = set()
        for clause in clauses:
            for literal in clause:
                variables.add(abs(literal))
        variables = sorted(variables)
        
        indicator = 0
        min_distance = float('inf')
        for clause in clauses:
            for literal in clause:
                index = variables.index(abs(literal)) - 1
                if (indicator >> index) & 1 == 0:
                    indicator |= 1 << index
                    for j in range(index):
                        if ((indicator >> j) & 1) != 0 and abs(variables[index] - variables[j]) < min_distance:
                            min_distance = abs(variables[index] - variables[j])
        return math.log(min_distance)
    
    def resolution_width(clauses):
        n = len(variables)
        clauses = [[abs(lit) for lit in clause] for clause in clauses]
        
        def dpll(clauses, assignment):
            if not clauses:
                return 0
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if literal in assignment and assignment[literal]:
                    return float('inf')
                new_clauses = [c for c in clauses if literal not in c]
                if -literal in new_clauses:
                    new_clauses.remove(-literal)
                width = dpll(new_clauses, new_assignment)
                if width == float('inf'):
                    return float('inf')
                new_assignment[literal] = False
                new_clauses = [c for c in clauses if literal not in c]
                if -literal in new_clauses:
                    new_clauses.remove(-literal)
                width += 1
                return width
            pure_literal = next((l for l in variables if (l not in assignment and -l not in assignment)), None)
            if pure_literal is None:
                return float('inf')
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            new_clauses = [c for c in clauses if pure_literal not in c]
            if -pure_literal in new_clauses:
                new_clauses.remove(-pure_literal)
            width = dpll(new_clauses, new_assignment)
            if width == float('inf'):
                return float('inf')
            new_assignment[pure_literal] = False
            new_clauses = [c for c in clauses if pure_literal not in c]
            if -pure_literal in new_clauses:
                new_clauses.remove(-pure_literal)
            width += 1
            return width
        
        return dpll(clauses, {})
    
    n_values = [5, 10, 15, 20, 30, 40]
    mrd_values = []
    width_values = []
    
    for n in n_values:
        phi = generate_formula(n)
        mrd_phi = mrd(phi)
        w_phi = resolution_width(phi)
        mrd_values.append(mrd_phi)
        width_values.append(w_phi)
    
    correlation_coefficient = 0
    if len(mrd_values) > 1 and len(width_values) > 1:
        mean_mrd = sum(mrd_values) / len(mrd_values)
        mean_width = sum(width_values) / len(width_values)
        numerator = sum((mrd_values[i] - mean_mrd) * (width_values[i] - mean_width) for i in range(len(mrd_values)))
        denominator = math.sqrt(sum((mrd_values[i] - mean_mrd)**2 for i in range(len(mrd_values))) * sum((width_values[i] - mean_width)**2 for i in range(len(width_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.7 <= correlation_coefficient <= 1.0,
        "counterexample": "" if 0.7 <= correlation_coefficient <= 1.0 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_outside_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")