# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, alpha):
        clauses = []
        for _ in range(int(alpha * n * (n - 1) / 2)):
            clause = [random.randint(0, 1) * 2 - 1 for _ in range(3)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def evaluate_formula(formula, assignment):
        return all(all((assignment[var] + lit) % 2 == 0 for var, lit in clause.items()) for clause in formula)
    
    def dpll(formula, assignment, literals, index=0):
        if not formula:
            return True
        if index == len(literals):
            return False
        
        literal = literals[index]
        pos_literal = abs(literal) - 1
        new_assignment = assignment[:]
        new_assignment[pos_literal] = (literal > 0)
        
        if dpll(formula, new_assignment, literals, index + 1):
            return True
        
        new_assignment[pos_literal] = not new_assignment[pos_literal]
        return dpll(formula, new_assignment, literals, index + 1)
    
    def leaf_count(formula, assignment, literals, index=0):
        if not formula:
            return 1
        if index == len(literals):
            return 0
        
        literal = literals[index]
        pos_literal = abs(literal) - 1
        new_assignment = assignment[:]
        new_assignment[pos_literal] = (literal > 0)
        
        count_true = leaf_count(formula, new_assignment, literals, index + 1)
        new_assignment[pos_literal] = not new_assignment[pos_literal]
        count_false = leaf_count(formula, new_assignment, literals, index + 1)
        
        return count_true + count_false
    
    def newton_inequality_defect(n, clauses):
        a_k = [0] * (n + 1)
        for assignment in product([0, 1], repeat=n):
            if evaluate_formula(clauses, dict(enumerate(assignment))):
                a_k[sum(assignment)] += 1
        
        delta = 0
        for k in range(1, n):
            a_k_minus_1 = a_k[k-1]
            a_k_plus_1 = a_k[k+1]
            a_k_current = a_k[k]
            
            if a_k_current == 0:
                continue
            
            term = max(0, (a_k_minus_1 * a_k_plus_1) / (a_k_current ** 2) - ((k-1)*(n-k+1)) / (k*(n-k+1)))
            delta = max(delta, term)
        
        return delta
    
    def generate_random_satisfiable_3cnf(n, alpha):
        while True:
            clauses = generate_3cnf(n, alpha)
            if any(evaluate_formula(clauses, dict(enumerate([random.randint(0, 1) for _ in range(n)]))) for _ in range(10)):
                return clauses
    
    n_values = [14, 16, 18, 20]
    alpha_values = [3.6, 3.8, 4.0]
    num_trials = 30
    c1, c2 = 0.25, 4
    
    results = []
    for n, alpha in product(n_values, alpha_values):
        total_s = 0
        total_r = 0
        count_fails = 0
        
        for _ in range(num_trials):
            clauses = generate_random_satisfiable_3cnf(n, alpha)
            delta = newton_inequality_defect(n, clauses)
            
            if delta == 0:
                results.append({"seed": seed, "n": n, "alpha": alpha, "conjecture_holds": False, "counterexample": "mapping_undefined"})
                continue
            
            assignment = [random.randint(0, 1) for _ in range(n)]
            leaf_count_value = leaf_count(clauses, assignment, list(range(1, n+1)))
            
            s = math.log2(leaf_count_value) - c1 * n * math.log2(1 + delta) + c2 * math.sqrt(n)
            r = 0.55  # Placeholder value, will be updated later
            
            if s < -3:
                count_fails += 1
                results.append({"seed": seed, "n": n, "alpha": alpha, "conjecture_holds": False, "counterexample": f"s={s:.2f}, r={r:.2f}"})
                continue
            
            total_s += s
        
        if count_fails > 0:
            results.append({"seed": seed, "n": n, "alpha": alpha, "conjecture_holds": False, "counterexample": f"count_fails={count_fails}"})
            continue
        
        mean_s = total_s / num_trials
        r_values = []
        
        for _ in range(num_trials):
            clauses = generate_random_satisfiable_3cnf(n, alpha)
            delta = newton_inequality_defect(n, clauses)
            
            if delta == 0:
                continue
            
            assignment = [random.randint(0, 1) for _ in range(n)]
            leaf_count_value = leaf_count(clauses, assignment, list(range(1, n+1)))
            
            s = math.log2(leaf_count_value) - c1 * n * math.log2(1 + delta) + c2 * math.sqrt(n)
            r_values.append(s / mean_s)
        
        if len(r_values) > 0:
            r = sum(r_values) / len(r_values)
            results.append({"seed": seed, "n": n, "alpha": alpha, "conjecture_holds": r >= 0.55, "counterexample": ""})
    
    return {
        "metric_name": "s_value",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")