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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate clauses for each literal
        for lit in literals:
            clauses.append([lit])
        
        # Generate clauses for implications
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([f'-x{i}', f'x{j}'])
                clauses.append([f'-x{j}', f'x{i}'])
        
        # Generate the final clause
        final_clause = [f'-x{i}' for i in range(1, n+1)]
        clauses.append(final_clause)
        
        return literals, clauses
    
    def evaluate_formula(clause, assignment):
        return any(lit[0] == '-' and not assignment[int(lit[1:]) - 1] or lit[0] != '-' and assignment[int(lit) - 1] for lit in clause)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment[:]
            new_assignment[int(literal[1:]) - 1] = literal[0] == '-'
            return dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment)
        
        literal = random.choice(clauses[0])
        new_assignment = assignment[:]
        new_assignment[int(literal[1:]) - 1] = literal[0] == '-'
        if dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment):
            return True
        new_assignment[int(literal[1:]) - 1] = literal[0] != '-'
        return dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment)
    
    def compute_p_adic_valuation_width(formula):
        n = len(formula)
        values = []
        
        for i in range(2**n):
            assignment = [bool(i & (1 << j)) for j in range(n)]
            value = evaluate_formula(formula, assignment)
            if value:
                p_adic_val = 0
                while i % 2 == 0:
                    i //= 2
                    p_adic_val += 1
                values.append(p_adic_val)
        
        return min(values) if values else 0
    
    def compute_resolution_proof_width(formula):
        literals, clauses = formula
        n = len(literals)
        
        def resolve(clause1, clause2):
            new_clauses = []
            for lit1 in clause1:
                for lit2 in clause2:
                    if abs(int(lit1)) == abs(int(lit2)):
                        continue
                    new_lit = f'-{int(lit1)}' if int(lit1) * int(lit2) < 0 else str(abs(int(lit1)))
                    new_clause = [l for l in clause1 + clause2 if l != lit1 and l != lit2]
                    new_clause.append(new_lit)
                    new_clauses.append(new_clause)
            return new_clauses
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_assignment = assignment[:]
                new_assignment[int(literal[1:]) - 1] = literal[0] == '-'
                return dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment)
            
            literal = random.choice(clauses[0])
            new_assignment = assignment[:]
            new_assignment[int(literal[1:]) - 1] = literal[0] == '-'
            if dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment):
                return True
            new_assignment[int(literal[1:]) - 1] = literal[0] != '-'
            return dpll([c for c in clauses if not evaluate_formula(c, new_assignment)], new_assignment)
        
        proof_width = 0
        while clauses:
            clause = random.choice(clauses)
            clauses.remove(clause)
            new_clauses = []
            for other_clause in clauses:
                if any(lit in clause and lit[0] == '-' != other_lit[0] for lit, other_lit in zip(clause, other_clause)):
                    new_clauses.extend(resolve(clause, other_clause))
            clauses.extend(new_clauses)
            proof_width += 1
        
        return proof_width
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    
    mvw = compute_p_adic_valuation_width(formula)
    wp = compute_resolution_proof_width(formula)
    
    return {
        "metric_name": "correlation",
        "metric_value": Fraction(mvw * wp).limit_denominator(),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mvw * wp > 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.7) / len(results)
    
    if all(r >= 0.7 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_less_than_0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")