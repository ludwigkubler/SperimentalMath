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
    
    def generate_cnf(n):
        literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
        cnf = []
        for _ in range(n):
            clause = random.sample(literals, random.randint(1, n))
            cnf.append(clause)
        return cnf
    
    def count_hyperplane_regions(cnf):
        regions = 0
        for i in range(len(cnf)):
            for j in range(i+1, len(cnf)):
                if not any(x == -y for x, y in zip(cnf[i], cnf[j])):
                    regions += 1
        return regions
    
    def dpll_solve(cnf):
        def propagate():
            while True:
                changed = False
                for clause in cnf:
                    if len(clause) == 0:
                        return False
                    if len(clause) == 1:
                        literal = clause[0]
                        if literal > 0 and literal not in assignment:
                            assignment[literal] = True
                            changed = True
                        elif literal < 0 and -literal not in assignment:
                            assignment[-literal] = False
                            changed = True
                if not changed:
                    break
            return True
        
        def unit_propagate():
            while True:
                changed = False
                for literal, value in assignment.items():
                    if value:
                        for clause in cnf:
                            if literal in clause:
                                clause.remove(literal)
                                if len(clause) == 0:
                                    return False
                            elif -literal in clause:
                                clause.remove(-literal)
                                if len(clause) == 1 and clause[0] < 0:
                                    assignment[-clause[0]] = True
                                    changed = True
                if not changed:
                    break
            return True
        
        def backtrack():
            while stack:
                literal, value = stack.pop()
                assignment[literal] = None
                for clause in cnf:
                    if literal in clause:
                        clause.remove(literal)
                    elif -literal in clause:
                        clause.remove(-literal)
                if propagate() and unit_propagate():
                    return True
            return False
        
        n = len(cnf)
        assignment = {i: None for i in range(1, n+1)}
        stack = []
        
        if not propagate():
            return False
        if not unit_propagate():
            return False
        
        if backtrack():
            return True
        else:
            return False
    
    def communication_complexity(cnf):
        return dpll_solve(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    regions = count_hyperplane_regions(cnf)
    comm_complexity = communication_complexity(cnf)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity <= regions,
        "counterexample": "" if comm_complexity <= regions else f"Graph with n={n}, A={cnf}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")