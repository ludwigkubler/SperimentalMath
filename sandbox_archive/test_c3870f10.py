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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def tropicalize(poly, variables):
        n = len(variables)
        mhr = 0
        for term in poly.split(' + '):
            if not term:
                continue
            degree = sum(term.count(var) for var in variables)
            mhr = max(mhr, degree)
        return mhr
    
    def dpll(phi):
        literals = phi.split(' or ')
        n = len(literals)
        
        def solve(assignment):
            unsatisfied = [lit for lit in literals if not evaluate(lit, assignment)]
            if not unsatisfied:
                return True
            literal = unsatisfied[0]
            var = literal[1] if literal[0] == '¬' else literal[0]
            pos_literal = literal if literal[0] != '¬' else literal[1:]
            neg_literal = '¬' + literal if literal[0] != '¬' else literal[1:]
            assignment[var] = True
            if solve(assignment):
                return True
            assignment[var] = False
            assignment[neg_literal] = True
            if solve(assignment):
                return True
            del assignment[var]
            del assignment[neg_literal]
            return False
        
        def evaluate(lit, assignment):
            if lit[0] == '¬':
                var = lit[1:]
                return not assignment.get(var, False)
            else:
                return assignment.get(lit, False)
        
        assignment = {}
        return solve(assignment)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed are sampled
            variables = [f'x{i}' for i in range(n)]
            clauses = []
            for _ in range(n):
                clause = random.choice(variables) + ' or ' + random.choice(variables)
                clauses.append(clause)
            phi = ' or '.join(clauses)
            
            mhr = tropicalize(phi, variables)
            w_phi = 1 if dpll(phi) else float('inf')
            
            total_metric_value += mhr / w_phi
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = total_metric_value / instances_tested <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mhr/w_ratio",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")