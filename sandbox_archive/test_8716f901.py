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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = []
        for _ in range(3):
            var = random.randint(1, n)
            sign = random.choice(['', '¬'])
            clause.append(f"{sign}x{var}")
        cnf.append(" ∧ ".join(clause))
    return " ∨ ".join(cnf)

def is_unsatisfiable(cnf):
    def eval_clause(clause, assignment):
        for literal in clause.split(' ∨ '):
            var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
            sign = 1 if literal.startswith('x') else -1
            if assignment[var] == sign:
                return True
        return False

    def eval_cnf(cnf, assignment):
        return all(eval_clause(clause, assignment) for clause in cnf.split(' ∧ '))

    n = max(int(literal[2:]) if literal.startswith('x') else int(literal[3:]) for literal in cnf.replace(' ∨ ', ' ').replace(' ∧ ', ' '))
    assignment = {i: random.choice([1, -1]) for i in range(1, n + 1)}
    
    max_steps = 60
    for _ in range(max_steps):
        if eval_cnf(cnf, assignment):
            return False
        var = random.randint(1, n)
        sign = assignment[var]
        assignment[var] = -sign
    
    return True

def walsh_transform(p_F, S):
    n = len(p_F)
    result = 0
    for C in range(2**n):
        if bin(C).count('1') == len(S):
            subset_vars = [i + 1 for i, bit in enumerate(bin(C)[2:].zfill(n)) if bit == '1']
            sign = (-1)**sum(p_F[i] for i in subset_vars if i not in S)
            result += sign * (2 ** -len(subset_vars))
    return result

def compute_T(F, p_F):
    n = len(p_F)
    T = 0
    for i in range(1, n + 1):
        for S in combinations(range(n), min(i, 3)):
            T += math.sqrt(walsh_transform(p_F, S) ** 2)
    return T

def dpll(cnf, assignment, unit_propagate=True):
    def is_clause_satisfied(clause, assignment):
        return any(assignment[var] == (literal.startswith('x') and 1 or -1) for literal in clause.split(' ∨ '))

    def propagate():
        while True:
            changed = False
            for var, sign in assignment.items():
                if sign != 0:
                    continue
                unit_clauses = [clause for clause in cnf if is_clause_satisfied(clause, assignment)]
                if len(unit_clauses) == 1:
                    literal = unit_clauses[0].split(' ∨ ')[0]
                    var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
                    sign = 1 if literal.startswith('x') else -1
                    assignment[var] = sign
                    changed = True
            if not changed:
                break

    def backtrack():
        nonlocal assignment, stack
        while stack and assignment[stack[-1]] == -assignment[stack[-1]]:
            stack.pop()
        if not stack:
            return False
        var = stack[-1]
        sign = assignment[var]
        assignment[var] = 0
        stack.append(var)
        assignment[var] = -sign
        return True

    propagate()
    stack = []
    while True:
        unit_clauses = [clause for clause in cnf if is_clause_satisfied(clause, assignment)]
        if len(unit_clauses) == 1:
            literal = unit_clauses[0].split(' ∨ ')[0]
            var = int(literal[2:]) if literal.startswith('x') else int(literal[3:])
            sign = 1 if literal.startswith('x') else -1
            assignment[var] = sign
        elif any(not is_clause_satisfied(clause, assignment) for clause in cnf):
            if not backtrack():
                return False
        else:
            break

    return sum(assignment[var] != 0 for var in range(1, len(p_F) + 1))

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [16, 20, 24, 28, 32]
    alpha_values = [4.0, 4.5, 5.0]
    instances_tested = 0
    log_2_1_plus_B_F_sum = 0
    T_F_over_sqrt_m_sum = 0
    
    for n in n_values:
        m = math.ceil(alpha_values[0] * n)
        cnf = generate_cnf(n, m)
        
        if not is_unsatisfiable(cnf):
            continue
        
        p_F = [0] * (n + 1)
        for i in range(1, n + 1):
            p_F[i] = sum((-1)**sum(p_F[j] for j in range(i) if j != k) * 2**-len(bin(k)[2:].zfill(n)) for k in range(2**n))
        
        T_F = compute_T(cnf, p_F)
        B_F = dpll(cnf, [0] * (n + 1), unit_propagate=True)
        
        if B_F == 0:
            continue
        
        log_2_1_plus_B_F = math.log2(1 + B_F)
        T_F_over_sqrt_m = T_F / math.sqrt(m)
        
        instances_tested += 1
        log_2_1_plus_B_F_sum += log_2_1_plus_B_F
        T_F_over_sqrt_m_sum += T_F_over_sqrt_m
        
        if log_2_1_plus_B_F < 0.10 * T_F_over_sqrt_m:
            return {
                "metric_name": "log_2(1+B(F)) vs T(F)/sqrt(m)",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={m}, log_2(1+B(F))={log_2_1_plus_B_F}, T(F)/sqrt(m)={T_F_over_sqrt_m}"
            }
    
    if instances_tested == 0:
        return {
            "metric_name": "log_2(1+B(F)) vs T(F)/sqrt(m)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "no unsatisfiable instances generated"
        }
    
    mean_log_2_1_plus_B_F = log_2_1_plus_B_F_sum / instances_tested
    mean_T_F_over_sqrt_m = T_F_over_sqrt_m_sum / instances_tested
    
    return {
        "metric_name": "log_2(1+B(F)) vs T(F)/sqrt(m)",
        "metric_value": None,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
        results.append(trial)
    
    if all("conjecture_holds" in result and result["conjecture_holds"] for result in results):
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_log_2_1_plus_B_F} std={math.sqrt(sum((result['metric_value'] - mean_log_2_1_plus_B_F) ** 2 for result in results)) / len(results)} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result and result["counterexample"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")