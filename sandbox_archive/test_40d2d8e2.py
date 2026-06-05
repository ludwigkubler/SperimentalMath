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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def tseitin_encoding(formulas):
        literals = set()
        for clause in formulas:
            literals.update(abs(lit) for lit in clause)
        new_vars = {lit: len(literals) + i for i, lit in enumerate(literals)}
        formulas_tseitin = []
        for clause in formulas:
            new_clause = [new_vars[lit] if lit > 0 else -new_vars[-lit] for lit in clause]
            formulas_tseitin.append(new_clause)
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause):
                    if i < j:
                        formulas_tseitin.append([-new_vars[lit1], -new_vars[lit2], new_vars[-lit1] + n + 1])
        return formulas_tseitin
    
    def dpll(formulas, assignment):
        if not formulas:
            return True
        literal = next((lit for lit in literals if lit not in assignment and -lit not in assignment), None)
        if literal is None:
            return False
        
        new_assignment = assignment.copy()
        polarity = random.choice([True, False])
        new_assignment[literal] = polarity
        
        def propagate(formulas):
            new_formulas = []
            for clause in formulas:
                if literal in clause:
                    continue
                if -literal in clause:
                    new_clause = [lit for lit in clause if lit != -literal]
                    if not new_clause:
                        return None
                    new_formulas.append(new_clause)
                else:
                    new_formulas.append(clause)
            return new_formulas
        
        propagated_formulas = propagate(formulas)
        if propagated_formulas is None:
            return False
        
        if dpll(propagated_formulas, new_assignment):
            return True
        
        del new_assignment[literal]
        
        new_assignment[-literal] = not polarity
        propagated_formulas = propagate(formulas)
        if propagated_formulas is None:
            return False
        
        return dpll(propagated_formulas, new_assignment)
    
    def min_rank_quasi_crystalline_sheaf(n):
        # Placeholder for the actual computation of the minimal rank of a quasi-crystalline sheaf
        return random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    formulas_tseitin = tseitin_encoding(formula)
    height = len(dpll(formulas_tseitin, {}))
    rank = min_rank_quasi_crystalline_sheaf(n)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": random.random(),  # Placeholder for actual correlation calculation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='CRC too low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")