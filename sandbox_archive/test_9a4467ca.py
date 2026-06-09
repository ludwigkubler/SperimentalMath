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

def random_cnf(n: int, m: int) -> list:
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, n)
            if random.choice([True, False]):
                clause.add(-var)
            else:
                clause.add(var)
        cnf.append(list(clause))
    return cnf

def dpll(cnf: list, assignment: dict):
    def solve():
        unassigned = [v for v in range(1, len(cnf) + 1) if v not in assignment and -v not in assignment]
        if not unassigned:
            if all(all(lit in assignment and (assignment[lit] == True if lit > 0 else False) for lit in clause) for clause in cnf):
                return assignment
            else:
                return None

        var = unassigned[0]
        assignment[var] = True
        result = solve()
        if result is not None:
            return result
        del assignment[var]
        assignment[-var] = True
        result = solve()
        if result is not None:
            return result
        del assignment[-var]
        return None

    return solve()

def resolution_width(cnf: list) -> int:
    def resolve(clause1, clause2):
        for lit1 in clause1:
            if -lit1 in clause2:
                new_clause = [l for l in clause1 if l != lit1] + [l for l in clause2 if l != -lit1]
                return new_clause
        return None

    def dpll_resolution(cnf):
        queue = cnf[:]
        while True:
            unit_clauses = [c for c in queue if len(c) == 1]
            if not unit_clauses:
                break
            unit_lit, _ = unit_clauses[0]
            queue = [c for c in queue if unit_lit not in c and -unit_lit not in c]
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    new_clause = resolve(queue[i], queue[j])
                    if new_clause:
                        queue.append(new_clause)
        return len(queue)

    return dpll_resolution(cnf)

def renyi_divergence(p: list, q: list, alpha: float) -> Fraction:
    if alpha == 1:
        return sum((p_i - q_i).log() for p_i, q_i in zip(p, q))
    else:
        return (sum(p_i**alpha * q_i**(1-alpha) for p_i, q_i in zip(p, q)) / (alpha - 1)).log()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n * 2)
    cnf = random_cnf(n, m)
    
    p = [Fraction(1, 2**n)] * (2**n)
    q = [sum(1 for clause in cnf if all(lit in assignment and (assignment[lit] == True if lit > 0 else False) for lit in clause)) / (2**n) for assignment in itertools.product([True, False], repeat=n)]
    
    max_width = 0
    total_width = 0
    instances_tested = 0
    
    for alpha in [1, float('inf')]:
        if alpha == float('inf'):
            alpha_val = '∞'
        else:
            alpha_val = str(alpha)
        
        width = resolution_width(cnf)
        max_width = max(max_width, width)
        total_width += width
        instances_tested += 1
        
        p_dist = [Fraction(1, 2**n)] * (2**n)
        q_dist = [sum(1 for clause in cnf if all(lit in assignment and (assignment[lit] == True if lit > 0 else False) for lit in clause)) / (2**n) for assignment in itertools.product([True, False], repeat=n)]
        
        divergence = renyi_divergence(p_dist, q_dist, alpha)
        if divergence <= Fraction(1, 1):
            conjecture_holds = True
            counterexample = ""
        else:
            conjecture_holds = False
            counterexample = f"alpha={alpha_val}, D_α={divergence}, w(φ)={width}"
    
    mean_width = total_width / instances_tested
    std_deviation = (sum((width - mean_width)**2 for width in range(max_width + 1)) / instances_tested).sqrt()
    
    return {
        "metric_name": "Resolution Width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max_width,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)).sqrt()
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")