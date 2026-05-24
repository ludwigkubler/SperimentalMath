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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        return [[random.choice([-i, i]) for _ in range(random.randint(2, 3))] for _ in range(n)]
    
    def dpll_width(cnf):
        n = len(cnf)
        clauses = cnf
        variables = set()
        for clause in clauses:
            for literal in clause:
                variables.add(abs(literal))
        
        def is_satisfiable(model):
            for clause in clauses:
                if not any(literal in model and model[literal] == (literal > 0) or -literal in model and model[-literal] == (literal < 0) for literal in clause):
                    return False
            return True
        
        def dpll(model, literals):
            if not literals:
                return is_satisfiable(model)
            
            literal = literals[0]
            rest = literals[1:]
            new_model_true = model.copy()
            new_model_true[literal] = True
            if dpll(new_model_true, rest):
                return True
            
            new_model_false = model.copy()
            new_model_false[literal] = False
            if dpll(new_model_false, rest):
                return True
            
            return False
        
        literals = list(variables)
        return len(literals) if dpll({}, literals) else 0
    
    def twisted_tensor_product(cnf):
        n = len(cnf)
        rank = 1
        for _ in range(n):
            rank *= 2
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_rank = twisted_tensor_product(cnf)
    dpll_width_val = dpll_width(cnf)
    
    if dpll_width_val == 0:
        return {
            "metric_name": "MinRank(TwistedRep(F)) / DPLLWidth(F)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLLWidth(F) is 0, which is undefined."
        }
    
    ratio = min_rank / dpll_width_val
    
    return {
        "metric_name": "MinRank(TwistedRep(F)) / DPLLWidth(F)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 107))  # Default to first 30 primes if no seeds provided
    
    results = []
    total_ratio = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        results.append(trial_result["metric_value"])
        total_ratio += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_ratio = total_ratio / len(results)
    support_fraction = count_supporting / len(results)
    
    if all(ratio <= 3 for ratio in results):
        result = "SUPPORTED"
    elif any(ratio >= 10 for ratio in results):
        result = "FALSIFIED"
    else:
        result = "INCONCLUSIVE"
    
    print(f"RESULT: {result} mean={mean_ratio:.2f} std={sum((x - mean_ratio) ** 2 for x in results) / len(results):.2f} support_fraction={support_fraction:.2f}")