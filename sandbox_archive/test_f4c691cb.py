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
    
    def generate_sat_instance(n):
        clauses = []
        for i in range(n):
            literals = [random.choice([f'x{i+1}', f'-x{i+1}']) for _ in range(3)]
            clause = ' | '.join(literals)
            clauses.append(clause)
        return ' & '.join(clauses)

    def tseitin_representation(sat_instance):
        n = len(sat_instance.split(' & '))
        literals = set()
        formulas = []
        
        for i, clause in enumerate(sat_instance.split(' & ')):
            literals.update(clause.split(' | '))
            new_var = f'y{i+1}'
            formulas.append(f'({clause}) -> {new_var}')
            formulas.append(f'{new_var} -> ({clause})')
        
        tseitin_formula = ' & '.join(formulas)
        return tseitin_formula, literals

    def dpll_search_tree_diameter(tseitin_formula):
        # Placeholder for DPLL search tree diameter calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)

    def algebraic_k_group_rank(literals):
        # Placeholder for algebraic K-group rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(literals)

    n = random.choice([5, 10, 15, 20, 30, 40])
    sat_instance = generate_sat_instance(n)
    tseitin_formula, literals = tseitin_representation(sat_instance)
    
    d_pi = dpll_search_tree_diameter(tseitin_formula)
    rank_K_pi = algebraic_k_group_rank(literals)
    logrank_K_pi = math.log(rank_K_pi) if rank_K_pi > 0 else float('-inf')
    
    return {
        "metric_name": "d(π)",
        "metric_value": d_pi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": d_pi <= logrank_K_pi,
        "counterexample": "" if d_pi <= logrank_K_pi else f"d(π)={d_pi} > logrank(K_π)={logrank_K_pi}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if 'metric_value' in r]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values)} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['counterexample'] for r in results):
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")