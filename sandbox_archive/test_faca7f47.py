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
    
    def dpll_solve(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        literals = [i for i in range(1, n + 1)] + [-i for i in range(1, n + 1)]
        
        def is_satisfiable(model):
            for clause in cnf:
                if all(lit not in model or model[lit] != (lit > 0) for lit in clause):
                    return False
            return True
        
        def backtrack(model, literals):
            if len(model) == n:
                return is_satisfiable(model)
            literal = literals[0]
            if backtrack(model | {literal: True}, literals[1:]):
                return True
            if backtrack(model | {literal: False}, literals[1:]):
                return True
            return False
        
        return backtrack({}, literals)
    
    def formal_context(cnf):
        minterms = set()
        non_minterms = set()
        for clause in cnf:
            if len(clause) == 1:
                minterms.add(clause[0])
            else:
                non_minterms.add(tuple(sorted(clause)))
        
        universe = list(minterms) + list(non_minterms)
        R = {}
        for x in universe:
            R[x] = set()
        
        for clause in cnf:
            if len(clause) == 1:
                continue
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    R[clause[i]].add(clause[j])
                    R[clause[j]].add(clause[i])
        
        return universe, R
    
    def min_rank(universe, R):
        n = len(universe)
        rank = [0] * n
        visited = [False] * n
        
        for i in range(n):
            if not visited[i]:
                queue = [i]
                while queue:
                    u = queue.pop(0)
                    if not visited[u]:
                        visited[u] = True
                        for v in R[universe[u]]:
                            rank[v] += 1
                            queue.append(v)
        
        return max(rank)
    
    def generate_cnf(n, m):
        cnf = []
        literals = list(range(1, n + 1)) + [-i for i in range(1, n + 1)]
        random.shuffle(literals)
        for _ in range(m):
            clause = [literals.pop() for _ in range(random.randint(2, 3))]
            cnf.append(clause)
        return cnf
    
    def width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        max_width = 0
        while clauses:
            unit_clauses = [clause for clause in clauses if len(clause) == 1]
            if not unit_clauses:
                break
            literal = unit_clauses[0][0]
            new_clauses = set()
            for clause in clauses:
                if literal not in clause and -literal not in clause:
                    new_clauses.add(tuple(sorted(set(clause) - {literal, -literal})))
            max_width += 1
            clauses = new_clauses
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            if not dpll_solve(cnf):
                continue
            universe, R = formal_context(cnf)
            min_rank_value = min_rank(universe, R)
            width_value = width(cnf)
            results.append((min_rank_value, math.log(width_value)))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_metric = sum(value for _, value in results) / len(results)
    std_metric = math.sqrt(sum((value - mean_metric) ** 2 for _, value in results) / len(results))
    correlation_coefficient = sum((min_rank_value - mean_metric) * (math.log(width_value) - mean_metric) for min_rank_value, width_value in results) / (len(results) * std_metric * std_metric)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9 and all(abs(min_rank_value - math.log(width_value)) <= 5 for min_rank_value, width_value in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3**j + 5**k for i in range(10) for j in range(10) for k in range(10)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result["metric_value"])
    
    mean_metric = sum(results) / len(results)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x is not None and x > 0.9) / len(results)
    
    if all(x is not None and x > 0.9 for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(x is not None and x <= 0.9 for x in results) or any(abs(x - math.log(y)) > 5 for x, y in zip(results, [math.exp(math.log(y)) for y in range(1, len(results) + 1)])):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={seeds[results.index(min(results, key=lambda x: abs(x - 0.9)))]}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_data")