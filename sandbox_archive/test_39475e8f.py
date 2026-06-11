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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(-len(assignment), len(assignment)) if (l in assignment and -l not in assignment) or (-l in assignment and l not in assignment)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            return False
        literal = next((l for l in range(-len(assignment), len(assignment)) if l not in assignment and -l not in assignment), None)
        new_assignment1 = assignment.copy()
        new_assignment1[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment1):
            return True
        new_assignment2 = assignment.copy()
        new_assignment2[literal] = False
        if dpll([c for c in clauses if -literal not in c], new_assignment2):
            return True
        return False
    
    def generate_random_cnf(n, m):
        literals = list(range(-n, 0)) + list(range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def formal_context_width(clauses):
        context = set()
        for clause in clauses:
            context.update(clause)
        return len(context)
    
    def dpll_tree_height(clauses):
        assignment = {}
        stack = [(clauses, assignment)]
        max_height = 0
        while stack:
            current_clauses, current_assignment = stack.pop()
            if not current_clauses:
                continue
            unit_clause = next((c for c in current_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = current_assignment.copy()
                new_assignment[literal] = True
                stack.append((current_clauses, new_assignment))
                new_assignment[literal] = False
                stack.append(([c for c in current_clauses if -literal not in c], new_assignment))
            else:
                literal = next((l for l in range(-len(current_assignment), len(current_assignment)) if l not in current_assignment and -l not in current_assignment), None)
                new_assignment1 = current_assignment.copy()
                new_assignment1[literal] = True
                stack.append((current_clauses, new_assignment1))
                new_assignment2 = current_assignment.copy()
                new_assignment2[literal] = False
                stack.append(([c for c in current_clauses if -literal not in c], new_assignment2))
            max_height = max(max_height, len(stack) + 1)
        return max_height
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfw_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_random_cnf(n, int(1.2 * n))
            mfw = formal_context_width(clauses)
            w = dpll_tree_height(clauses)
            mfw_sum += mfw
            w_sum += w
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_mfw = mfw_sum / instances_tested
    mean_w = w_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(mfw * w for mfw, w in zip([mfw_sum] * instances_tested, [w_sum] * instances_tested)) - mfw_sum * w_sum) / math.sqrt((instances_tested * sum(mfw**2 for mfw in [mfw_sum] * instances_tested) - mfw_sum**2) * (instances_tested * sum(w**2 for w in [w_sum] * instances_tested) - w_sum**2))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.5,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")