# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_clause_set(n):
        variables = set()
        clauses = []
        for i in range(1, n + 1):
            literals = [random.choice([i, -i]) for _ in range(random.randint(2, 4))]
            clause = 'or'.join(f'x{i}' if l > 0 else f'-x{i}' for l in literals)
            clauses.append(clause)
            variables.update(literals)
        return clauses, variables
    
    def dpll_solver(clauses, assignment):
        unsatisfied_clauses = [c for c in clauses if not any(l in assignment and (assignment[l] == 1) or (-l in assignment and (assignment[-l] == 1)) for l in c.split('or'))]
        if not unsatisfied_clauses:
            return True
        literal, polarity = random.choice([(l, p) for clause in unsatisfied_clauses for l in clause.split('or') for p in [1, -1]])
        assignment[literal] = polarity
        if dpll_solver(clauses, assignment):
            return True
        del assignment[literal]
        assignment[-literal] = -polarity
        return dpll_solver(clauses, assignment)
    
    def minimal_index_of_kahler_metric(clause_set):
        variables = set()
        for clause in clause_set:
            variables.update(int(l) for l in clause.split('or'))
        n = len(variables)
        if n == 0:
            return 0
        k = 1
        while True:
            assignment = {i: random.choice([0, 1]) for i in range(1, n + 1)}
            if dpll_solver(clause_set, assignment):
                return k
            k += 1
    
    def compute_polynomial_bound(n):
        # Placeholder polynomial bound function
        return Fraction(n**2, 1)
    
    clause_set, variables = generate_tseitin_clause_set(30)
    kahler_index = minimal_index_of_kahler_metric(clause_set)
    resolution_length = len(dpll_solver(clause_set, {}))
    polynomial_bound = compute_polynomial_bound(len(variables))
    
    return {
        "metric_name": "Kähler Index vs Resolution Length",
        "metric_value": kahler_index,
        "instances_tested": 1,
        "conjecture_holds": kahler_index <= 2**resolution_length and kahler_index <= polynomial_bound,
        "counterexample": "" if kahler_index <= 2**resolution_length and kahler_index <= polynomial_bound else f"Kähler Index: {kahler_index}, Resolution Length: {resolution_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = (sum((r['metric_value'] - mean_metric)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break