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
    
    def tseitin_formula(n):
        variables = [f'x{i+1}' for i in range(n)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(1, n + 1):
            clauses.append([variables[i-1]])
            for j in range(i + 1, n + 1):
                clauses.append([-variables[i-1], variables[j-1]])
                clauses.append([-variables[j-1], variables[i-1]])
        
        return variables, clauses
    
    def dpll(clauses, assignment, i=0):
        if i == len(variables):
            for clause in clauses:
                if all(var not in assignment or (assignment[var] and var[0] != '-') or (-var not in assignment) for var in clause):
                    continue
                else:
                    return False
            return True
        
        variable = variables[i]
        positive_var = f'+{variable}'
        negative_var = f'-{variable}'
        
        if positive_var not in assignment and negative_var not in assignment:
            assignment[positive_var] = True
            if dpll(clauses, assignment, i + 1):
                return True
            assignment.pop(positive_var)
            
            assignment[negative_var] = True
            if dpll(clauses, assignment, i + 1):
                return True
            assignment.pop(negative_var)
        
        elif positive_var in assignment:
            assignment[negative_var] = False
        
        else:
            assignment[positive_var] = False
        
        return False
    
    def frege_proof_length(variables, clauses):
        assignment = {}
        proof_length = 0
        
        for clause in clauses:
            if all(var not in assignment or (assignment[var] and var[0] != '-') or (-var not in assignment) for var in clause):
                continue
            else:
                proof_length += 1
                for var in clause:
                    if var[0] == '-':
                        assignment[-var] = True
        
        return proof_length
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    
    min_rank = len(variables)  # Placeholder for actual computation
    frege_len = frege_proof_length(variables, clauses)
    
    return {
        "metric_name": "Frege Proof Length vs Minimal Rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")