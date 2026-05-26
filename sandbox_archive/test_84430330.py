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
    
    def tautology_degree(circuit):
        n = len(circuit['variables'])
        clauses = circuit['clauses']
        
        max_tautology_deg = 0
        for assignment in itertools.product([False, True], repeat=n):
            if all(any(l in assignment and assignment[l] == True for l in clause) for clause in clauses):
                max_tautology_deg += 1
        return max_tautology_deg
    
    def p_adic_valuation_rank(circuit):
        n = len(circuit['variables'])
        clauses = circuit['clauses']
        
        # Simplified DPLL solver to find a satisfying assignment
        def dpll(assignment, clause_set):
            if not clause_set:
                return True
            for literal in clause_set[0]:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if dpll(new_assignment, [c for c in clause_set if not any(l in c and c[l] == True for l in c)]):
                    return True
                new_assignment[literal] = False
                if dpll(new_assignment, [c for c in clause_set if not any(l in c and c[l] == False for l in c)]):
                    return True
            return False
        
        # Find a satisfying assignment
        assignment = {}
        if not dpll(assignment, clauses):
            return 0
        
        # Calculate p-adic valuation rank (simplified version)
        rank = 0
        for literal in assignment:
            if assignment[literal]:
                rank += 1
        return rank
    
    def generate_circuit(n, depth):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        
        def add_clause(clause):
            clauses.append(clause)
        
        def dnf(depth):
            if depth == 0:
                add_clause([random.choice(variables), random.choice(variables)])
            else:
                for _ in range(random.randint(1, 3)):
                    clause = [random.choice(variables)]
                    for _ in range(random.randint(1, 2)):
                        clause.append(random.choice(variables))
                    dnf(depth - 1)
        
        dnf(depth)
        return {'variables': variables, 'clauses': clauses}
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    depth = 2
    circuit = generate_circuit(n, depth)
    
    tautology_deg = tautology_degree(circuit)
    if tautology_deg == 0:
        return {
            "metric_name": "p-adic valuation rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit is unsatisfiable"
        }
    
    p_adic_rank = p_adic_valuation_rank(circuit)
    threshold = Fraction(1, tautology_deg)
    
    return {
        "metric_name": "p-adic valuation rank",
        "metric_value": p_adic_rank,
        "instances_tested": 1,
        "conjecture_holds": p_adic_rank <= threshold,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit with p-adic valuation rank greater than Θ(1/δ(C))\" first_failing_seed={first_failing_seed}")