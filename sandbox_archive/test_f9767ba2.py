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
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([f'x{i}', f'~x{i}']) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def tseitin(formulas):
        literals = set()
        new_vars = {}
        formulas_tseitin = []
        
        for clause in formulas:
            literals.update(clause)
            var = f'y{len(new_vars) + 1}'
            new_vars[var] = (clause, True)
            formulas_tseitin.append([var])
            for literal in clause:
                if literal.startswith('~'):
                    formulas_tseitin.append([literal[1:], var])
                else:
                    formulas_tseitin.append([f'~{literal}', f'~{var}'])
        
        return literals, new_vars, formulas_tseitin
    
    def dpll(formulas, assignment):
        if not formulas:
            return True
        literal, polarity = random.choice(formulas)
        if literal.startswith('~'):
            literal = literal[1:]
            polarity = not polarity
        
        if literal in assignment and assignment[literal] != polarity:
            return False
        
        new_assignment = assignment.copy()
        new_assignment[literal] = polarity
        
        for i, formula in enumerate(formulas):
            if literal in formula:
                formulas[i].remove(literal)
                if not formula:
                    return False
                if len(formula) == 1:
                    new_assignment[formula[0]] = ~polarity
        
        return dpll([f for f in formulas if literal not in f], new_assignment)
    
    def minimal_rank():
        # Placeholder for the actual computation of the minimal rank
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_formula(n)
            literals, new_vars, formulas_tseitin = tseitin(formula)
            height = len(dpll(formulas_tseitin, {}))
            rank = minimal_rank()
            metric_values.append((rank, height))
            instances_tested += 1
    
    if not metric_values:
        return {
            "metric_name": "Spearman's Rank Correlation Coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No data collected"
        }
    
    def spearman_correlation(values):
        ranks = {v: i for i, v in enumerate(sorted(set(v[0] for v in values)), start=1)}
        sorted_values = sorted([(ranks[v[0]], v[1]) for v in values], key=lambda x: x[0])
        n = len(sorted_values)
        
        ranks_y = [v[1] for v in sorted_values]
        rank_diffs_squared = sum((i - (n + 1) / 2) ** 2 for i, _ in enumerate(ranks_y))
        rho = 1 - (6 * sum(rank_diffs_squared)) / (n * (n**2 - 1))
        
        return rho
    
    rho = spearman_correlation(metric_values)
    
    return {
        "metric_name": "Spearman's Rank Correlation Coefficient",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": 0.5 < rho < 0.7,
        "counterexample": "" if 0.5 < rho < 0.7 else f"Spearman's rank correlation coefficient: {rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if 0.5 < r["metric_value"] < 0.7) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={math.sqrt(sum((r['metric_value'] - mean_rho) ** 2 for r in results if r['metric_value'] is not None) / len(results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Spearman\'s rank correlation coefficient < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data to support or refute the conjecture")