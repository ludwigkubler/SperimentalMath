# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                new_assignment[literal] = False
                if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                    return True
                else:
                    return False
        pure_literal = next((l for l in range(1, n+1) if all(l in c or -l in c for c in cnf)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                new_assignment[pure_literal] = False
                if dpll([c for c in cnf if pure_literal not in c and -pure_literal not in c], new_assignment):
                    return True
                else:
                    return False
        literal, _ = random.choice(cnf)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                return False
    
    def non_archimedean_valuation(cnf, assignment):
        valuation = 0
        for clause in cnf:
            if any(assignment.get(lit, False) for lit in clause):
                valuation += 1
        return valuation
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    assignment = {i: False for i in range(1, n+1)}
    
    depth = 0
    stack = [(cnf, assignment)]
    while stack:
        cnf, assignment = stack.pop()
        if not cnf:
            break
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0:
                literal = -literal
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            stack.append((cnf, new_assignment))
            break
        pure_literal = next((l for l in range(1, n+1) if all(l in c or -l in c for c in cnf)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            stack.append((cnf, new_assignment))
            break
        literal, _ = random.choice(cnf)
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        stack.append((cnf, new_assignment))
        break
    
    min_rank = non_archimedean_valuation(cnf, assignment)
    
    return {
        "metric_name": "min_rank_over_depth",
        "metric_value": Fraction(min_rank, depth),
        "instances_tested": 1,
        "conjecture_holds": 0.5 <= Fraction(min_rank, depth) <= 1.5,
        "counterexample": "" if 0.5 <= Fraction(min_rank, depth) <= 1.5 else f"min_rank={min_rank}, depth={depth}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")