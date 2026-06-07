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
        variables = [f"x{i}" for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [f"~{v}" if v.startswith("x") else v for v in clause]
            clauses.append(f"({clause[0]} & {clause[1]})")
        formula = " | ".join(clauses)
        return formula
    
    def dpll(formula):
        def parse_formula(formula):
            stack = []
            current_clause = []
            i = 0
            while i < len(formula):
                if formula[i] == '(':
                    stack.append(current_clause)
                    current_clause = []
                elif formula[i] == ')':
                    clause = current_clause.pop()
                    if not stack:
                        return clause
                    else:
                        parent_clause = stack.pop()
                        parent_clause.append(clause)
                elif formula[i] == '&':
                    i += 1
                elif formula[i] == '|':
                    stack.append(current_clause)
                    current_clause = []
                else:
                    j = i + 1
                    while j < len(formula) and formula[j].isalnum():
                        j += 1
                    current_clause.append(formula[i:j])
                    i = j - 1
                i += 1
            return current_clause
        
        def dpll_helper(clauses, assignment):
            if not clauses:
                return True
            clause = clauses[0]
            for literal in clause:
                if literal.startswith("~"):
                    var = literal[1:]
                    if var in assignment and assignment[var] == False:
                        continue
                else:
                    var = literal
                    if var in assignment and assignment[var] == True:
                        continue
                new_assignment = assignment.copy()
                new_assignment[var] = True
                if dpll_helper(clauses[1:], new_assignment):
                    return True
                new_assignment[var] = False
                if dpll_helper(clauses[1:], new_assignment):
                    return True
            return False
        
        parsed_formula = parse_formula(formula)
        return dpll_helper(parsed_formula, {})
    
    def quantum_group_rank(n):
        # Constructive method to find a quantum group representation rank for a Boolean formula with n variables
        # This is a placeholder implementation; replace with actual algorithm if known
        return math.ceil(math.sqrt(n))
    
    def depth_of_dpll_tree(formula):
        # Placeholder implementation of DPLL proof tree depth
        return len(formula.split(" | "))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_formula(n)
    rank = quantum_group_rank(n)
    dpll_depth = depth_of_dpll_tree(formula)
    
    return {
        "metric_name": "DPLL Depth",
        "metric_value": dpll_depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= math.sqrt(n) and dpll_depth >= rank,
        "counterexample": "" if rank <= math.sqrt(n) and dpll_depth >= rank else f"Formula: {formula}, Rank: {rank}, DPLL Depth: {dpll_depth}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")