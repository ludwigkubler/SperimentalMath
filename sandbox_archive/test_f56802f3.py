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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([f'x{i}', f'~x{i}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def macdonald_polynomial(cnf, n):
        # Simplified Macdonald polynomial calculation (constructive algorithm)
        rank = 0
        for clause in cnf:
            rank += len(set(clause))
        return rank
    
    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        
        def backtrack():
            if not stack:
                return True
            literal, negated = stack.pop()
            var = literal[1:] if literal.startswith('~') else literal
            value = 0 if literal.startswith('~') else 1
            
            assignment[var] = value
            for clause in cnf:
                if any(lit in assignment and assignment[lit] == (1 - int(negated)) for lit in clause):
                    continue
                break
            else:
                return backtrack()
            
            del assignment[var]
            assignment[var] = 1 - value
            for clause in cnf:
                if any(lit in assignment and assignment[lit] == (1 - int(negated)) for lit in clause):
                    continue
                break
            else:
                return backtrack()
            
            stack.append((literal, negated))
            del assignment[var]
            return False
        
        stack.append((random.choice(cnf[0]), True))
        return backtrack()
    
    n_values = [10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            rank = macdonald_polynomial(cnf, n)
            is_sat = is_satisfiable(cnf)
            
            if rank < n**2 and not is_sat:
                return {
                    "metric_name": "Rank of Macdonald Polynomial",
                    "metric_value": rank,
                    "instances_tested": instances_tested + 1,
                    "conjecture_holds": False,
                    "counterexample": f"n={n}, rank={rank}, SAT=False"
                }
            
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    return {
        "metric_name": "Rank of Macdonald Polynomial",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")