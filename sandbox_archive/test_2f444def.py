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
    
    def tseitin_encoding(formula):
        n = len(formula)
        new_vars = {}
        formulas_tseitin = []
        
        for i in range(n):
            if formula[i] not in new_vars:
                new_vars[formula[i]] = len(new_vars) + 1
            if -formula[i] not in new_vars:
                new_vars[-formula[i]] = len(new_vars) + 1
        
        def encode_clause(clause):
            literals = []
            for lit in clause:
                if lit > 0 and lit not in new_vars:
                    new_vars[lit] = len(new_vars) + 1
                elif lit < 0 and -lit not in new_vars:
                    new_vars[-lit] = len(new_vars) + 1
                literals.append(lit)
            return literals
        
        for clause in formula:
            literals = encode_clause(clause)
            if len(literals) == 2:
                formulas_tseitin.append([-new_vars[literals[0]], -new_vars[literals[1]], new_vars[-literals[0]] + n + 1])
                formulas_tseitin.append([new_vars[literals[0]], new_vars[literals[1]], -new_vars[-literals[0]] - n - 2])
            elif len(literals) == 3:
                formulas_tseitin.append([-new_vars[literals[0]], literals[1], literals[2]])
                formulas_tseitin.append([new_vars[literals[0]], -literals[1], literals[2]])
                formulas_tseitin.append([new_vars[literals[0]], literals[1], -literals[2]])
                formulas_tseitin.append([-new_vars[literals[0]], -literals[1], -literals[2]])
        
        return formulas_tseitin
    
    def dpll(formula):
        n = len(formula)
        assignment = [None] * (n + 1)
        
        def solve(i):
            if i == n:
                return True
            for val in [True, False]:
                assignment[i + 1] = val
                if all(lit <= 0 or (assignment[abs(lit)] is not None and assignment[abs(lit)] == (lit > 0)) for clause in formula):
                    if solve(i + 1):
                        return True
            assignment[i + 1] = None
            return False
        
        return solve(0)
    
    def minimal_rank(formula):
        n = len(formula)
        rank = 0
        for i in range(n):
            if all(lit <= 0 or (assignment[abs(lit)] is not None and assignment[abs(lit)] == (lit > 0)) for clause in formula):
                rank += 1
        return rank
    
    def spearman_correlation(ranks1, ranks2):
        n = len(ranks1)
        if n != len(ranks2):
            raise ValueError("Ranks lists must have the same length")
        
        sorted_ranks1 = sorted(range(n), key=lambda i: ranks1[i])
        sorted_ranks2 = sorted(range(n), key=lambda i: ranks2[i])
        
        rho_numerator = sum((sorted_ranks1[i] - sorted_ranks2[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        
        return 1 - (6 * rho_numerator) / rho_denominator
    
    n = random.randint(5, 40)
    formula = [random.choice([i, -i]) for _ in range(n)]
    
    formulas_tseitin = tseitin_encoding(formula)
    dpll_height = len(dpll(formulas_tseitin))
    minimal_rank_value = minimal_rank(formulas_tseitin)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": spearman_correlation([i for i in range(n)], [minimal_rank_value] * n),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='Spearman\'s rank correlation coefficient < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")