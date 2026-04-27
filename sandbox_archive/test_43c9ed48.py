# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def back_substitution(A):
    n = len(A)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def solve_linear_system(A, b):
    Ab = [row + [b[i]] for i, row in enumerate(A)]
    Ab = gaussian_elimination(Ab)
    return back_substitution(Ab)

def dpll(F, assignment, unit_propagate=True):
    if not F:
        return True
    if any(all(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in F):
        return False
    unit_clauses = [lit for lit in F[0] if lit not in assignment]
    if unit_clauses:
        lit = unit_clauses[0]
        assignment[lit] = True
        if dpll(F, assignment, unit_propagate):
            return True
        del assignment[lit]
        assignment[-lit] = True
        if dpll(F, assignment, unit_propagate):
            return True
        del assignment[-lit]
    else:
        lit = F[0][0]
        for val in [True, False]:
            assignment[lit] = val
            if dpll(F, assignment, unit_propagate):
                return True
            del assignment[lit]
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        c1, c2 = None, None
        total_V = 0.0
        total_gap = 0.0
        count = 0
        
        for _ in range(200):
            m = 4 * n
            F = [[random.choice([-i, i]) for i in range(1, n + 1)] for _ in range(m)]
            
            assignment = {}
            leaves = []
            def dpll_with_leaves(F, assignment, unit_propagate=True):
                if not F:
                    return True
                if any(all(lit in assignment and assignment[lit] == val for lit, val in clause) for clause in F):
                    return False
                unit_clauses = [lit for lit in F[0] if lit not in assignment]
                if unit_clauses:
                    lit = unit_clauses[0]
                    assignment[lit] = True
                    leaves.append(lit)
                    if dpll_with_leaves(F, assignment, unit_propagate):
                        return True
                    del assignment[lit]
                    assignment[-lit] = True
                    leaves.append(-lit)
                    if dpll_with_leaves(F, assignment, unit_propagate):
                        return True
                    del assignment[-lit]
                else:
                    lit = F[0][0]
                    for val in [True, False]:
                        assignment[lit] = val
                        leaves.append(lit if val else -lit)
                        if dpll_with_leaves(F, assignment, unit_propagate):
                            return True
                        del assignment[lit]
                return False
            
            dpll_with_leaves(F, assignment)
            
            X_F = math.log2(len(leaves))
            M_i = [X_F]
            V_F = 0.0
            
            for _ in range(30):
                F_est = F[:]
                for i in range(m):
                    if random.random() < 1 / (n * m):
                        F_est[i] = [random.choice([-j, j]) for j in range(1, n + 1)]
                assignment_est = {}
                def dpll_est_with_leaves(F_est, assignment_est, unit_propagate=True):
                    if not F_est:
                        return True
                    if any(all(lit in assignment_est and assignment_est[lit] == val for lit, val in clause) for clause in F_est):
                        return False
                    unit_clauses = [lit for lit in F_est[0] if lit not in assignment_est]
                    if unit_clauses:
                        lit = unit_clauses[0]
                        assignment_est[lit] = True
                        leaves_est = []
                        def dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate=True):
                            if not F_est:
                                return True
                            if any(all(lit in assignment_est and assignment_est[lit] == val for lit, val in clause) for clause in F_est):
                                return False
                            unit_clauses = [lit for lit in F_est[0] if lit not in assignment_est]
                            if unit_clauses:
                                lit = unit_clauses[0]
                                assignment_est[lit] = True
                                leaves_est.append(lit)
                                if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                    return True
                                del assignment_est[lit]
                                assignment_est[-lit] = True
                                leaves_est.append(-lit)
                                if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                    return True
                                del assignment_est[-lit]
                            else:
                                lit = F_est[0][0]
                                for val in [True, False]:
                                    assignment_est[lit] = val
                                    leaves_est.append(lit if val else -lit)
                                    if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                        return True
                                    del assignment_est[lit]
                            return False
                        
                        dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est)
                        M_i.append(math.log2(len(leaves_est)))
                    else:
                        lit = F_est[0][0]
                        for val in [True, False]:
                            assignment_est[lit] = val
                            leaves_est = []
                            def dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate=True):
                                if not F_est:
                                    return True
                                if any(all(lit in assignment_est and assignment_est[lit] == val for lit, val in clause) for clause in F_est):
                                    return False
                                unit_clauses = [lit for lit in F_est[0] if lit not in assignment_est]
                                if unit_clauses:
                                    lit = unit_clauses[0]
                                    assignment_est[lit] = True
                                    leaves_est.append(lit)
                                    if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                        return True
                                    del assignment_est[lit]
                                    assignment_est[-lit] = True
                                    leaves_est.append(-lit)
                                    if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                        return True
                                    del assignment_est[-lit]
                                else:
                                    lit = F_est[0][0]
                                    for val in [True, False]:
                                        assignment_est[lit] = val
                                        leaves_est.append(lit if val else -lit)
                                        if dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est, unit_propagate):
                                            return True
                                        del assignment_est[lit]
                                return False
                        
                        dpll_est_with_leaves_helper(F_est, assignment_est, leaves_est)
                        M_i.append(math.log2(len(leaves_est)))
                
                dpll_est_with_leaves(F_est, assignment_est)
            
            for i in range(1, len(M_i)):
                V_F += (M_i[i] - M_i[i-1])**2
            
            total_V += V_F
            max_gap = 0.0
            for i in range(m):
                F_alt = F[:]
                F_alt[i] = [random.choice([-j, j]) for j in range(1, n + 1)]
                assignment_alt = {}
                def dpll_alt_with_leaves(F_alt, assignment_alt, unit_propagate=True):
                    if not F_alt:
                        return True
                    if any(all(lit in assignment_alt and assignment_alt[lit] == val for lit, val in clause) for clause in F_alt):
                        return False
                    unit_clauses = [lit for lit in F_alt[0] if lit not in assignment_alt]
                    if unit_clauses:
                        lit = unit_clauses[0]
                        assignment_alt[lit] = True
                        leaves_alt = []
                        def dpll_alt_with_leaves_helper(F_alt, assignment_alt, leaves_alt, unit_propagate=True):
                            if not F_alt:
                                return True
                            if any(all(lit in assignment_alt and assignment_alt[lit] == val for lit, val in clause) for clause in F_alt):
                                return False
                            unit_clauses = [lit for lit in F_alt[0] if lit not in assignment_alt]
                            if unit_clauses:
                                lit = unit_clauses[0]
                                assignment_alt[lit] = True
                                leaves_alt.append(lit)
                                if dpll_alt_with_leaves_helper(F_alt, assignment_alt, leaves_alt, unit_propagate):
                                    return True
                                del assignment_alt[lit]
                                assignment_alt[-lit] = True
                                leaves_alt.append(-lit)
                                if dpll_alt_with_leaves_helper(F_alt, assignment_alt, leaves_alt, unit_propagate):
                                    return True
                                del assignment_alt[-lit]
                            else:
                                lit = F_alt[0][0]
                                for val in [True, False]:
                                    assignment_alt[lit] = val
                                    leaves_alt.append(lit if val else -lit)
                                    if dpll_alt_with_leaves_helper(F_alt, assignment_alt, leaves_alt, unit_propagate):
                                        return True
                                    del assignment_alt[lit]
                            return False
                        
                        dpll_alt_with_leaves_helper(F_alt, assignment_alt, leaves_alt)
                        X_F_alt = math.log2(len(leaves_alt))
                        max_gap = max(max_gap, abs(X_F - X_F_alt))
            
            total_gap += max_gap
            count += 1
        
        if c1 is None and c2 is None:
            c1 = 0.5 * (total_gap / count) / math.sqrt(total_V / count)
            c2 = 2.0 * (total_gap / count) / math.sqrt(total_V / count)
        
        results.append({
            "n": n,
            "V_F": total_V / count,
            "max_gap": total_gap / count
        })
    
    return {
        "metric_name": "Doob Variance Gap",
        "metric_value": sum(result["max_gap"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(c1 * math.sqrt(result["V_F"]) * math.log(result["n"]) <= result["max_gap"] <= c2 * math.sqrt(result["V_F"]) * math.log(result["n"]) for result in results),
        "counterexample": "" if all(c1 * math.sqrt(result["V_F"]) * math.log(result["n"]) <= result["max_gap"] <= c2 * math.sqrt(result["V_F"]) * math.log(result["n"]) for result in results) else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))