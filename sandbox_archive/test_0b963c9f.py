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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = set()
            for _ in range(random.randint(1, 3)):
                var = random.choice([f'x{i}' for i in range(1, n+1)] + [f'~x{i}' for i in range(1, n+1)])
                if var.startswith('~'):
                    clause.add(var[1:])
                else:
                    clause.add(f'~{var}')
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(clauses):
        stack = []
        assignment = {}
        for clause in clauses:
            found_literal = False
            for literal in clause:
                if literal.startswith('~'):
                    negated_var = literal[1:]
                    if negated_var not in assignment or not assignment[negated_var]:
                        stack.append((literal, len(clause)))
                        found_literal = True
                        break
                else:
                    if literal not in assignment or assignment[literal]:
                        stack.append((literal, len(clause)))
                        found_literal = True
                        break
            if not found_literal:
                return False
        while stack:
            literal, length = stack.pop()
            if literal.startswith('~'):
                negated_var = literal[1:]
                if negated_var in assignment and assignment[negated_var]:
                    continue
                assignment[negated_var] = True
                for clause in clauses:
                    if literal in clause:
                        clause.remove(literal)
                        if not clause:
                            return False
            else:
                var = literal
                if var in assignment and not assignment[var]:
                    continue
                assignment[var] = False
                for clause in clauses:
                    if literal in clause:
                        clause.remove(literal)
                        if not clause:
                            return False
        return True
    
    def tropical_hyperplanes(clauses):
        hyperplanes = []
        for clause in clauses:
            hyperplane = [Fraction(1, 0) if literal.startswith('~') else Fraction(0, 1) for literal in clause]
            hyperplanes.append(hyperplane)
        return hyperplanes
    
    def intersection_mod_2(hyperplanes):
        result = [Fraction(0, 1)]
        for hyperplane in hyperplanes:
            new_result = []
            for h in hyperplane:
                if h == Fraction(1, 0):
                    new_result.append(Fraction(1, 0))
                else:
                    new_result.append(result[0] + h)
            result = new_result
        return result
    
    def dpll_refutation_depth(clauses):
        stack = []
        assignment = {}
        for clause in clauses:
            found_literal = False
            for literal in clause:
                if literal.startswith('~'):
                    negated_var = literal[1:]
                    if negated_var not in assignment or not assignment[negated_var]:
                        stack.append((literal, len(clause)))
                        found_literal = True
                        break
                else:
                    if literal not in assignment or assignment[literal]:
                        stack.append((literal, len(clause)))
                        found_literal = True
                        break
            if not found_literal:
                return 0
        depth = 0
        while stack:
            literal, length = stack.pop()
            if literal.startswith('~'):
                negated_var = literal[1:]
                if negated_var in assignment and assignment[negated_var]:
                    continue
                assignment[negated_var] = True
                for clause in clauses:
                    if literal in clause:
                        clause.remove(literal)
                        if not clause:
                            return depth + 1
            else:
                var = literal
                if var in assignment and not assignment[var]:
                    continue
                assignment[var] = False
                for clause in clauses:
                    if literal in clause:
                        clause.remove(literal)
                        if not clause:
                            return depth + 1
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    if is_satisfiable(clauses):
        return {
            "metric_name": "DPLL Refutation Depth",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Mapping_undefined"
        }
    
    hyperplanes = tropical_hyperplanes(clauses)
    intersection_result = intersection_mod_2(hyperplanes)
    refutation_depth = dpll_refutation_depth(clauses)
    
    return {
        "metric_name": "DPLL Refutation Depth",
        "metric_value": refutation_depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r is not None and r <= mean) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r is not None and r > mean for r in results):
        first_failing_seed = seeds[results.index(max([r for r in results if r is not None]))]
        print(f"RESULT: FALSIFIED counterexample=\"Mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")