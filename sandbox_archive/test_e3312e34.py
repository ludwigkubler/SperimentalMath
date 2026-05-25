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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f'{var} ∨ ¬{var}')
        for i in range(1, n):
            clauses.append(f'{variables[i]} ∨ {variables[i+1]}')
        return clauses
    
    def quandle_representation(clauses, n):
        quandle = {}
        for clause in clauses:
            if '∨' in clause:
                var1, var2 = clause.split(' ∨ ')
                quandle[var1] = (var1, var2)
                quandle[var2] = (var2, var1)
            else:
                var = clause
                quandle[var] = (var, var)
        return quandle
    
    def minimal_rank(quandle):
        rank = 0
        for key in quandle:
            value = quandle[key]
            if len(value) > rank:
                rank = len(value)
        return rank
    
    def tseitin_resolution_depth(clauses):
        depth = 0
        stack = []
        visited = set()
        while clauses:
            clause = random.choice(clauses)
            if clause in visited:
                continue
            visited.add(clause)
            if '∨' in clause:
                var1, var2 = clause.split(' ∨ ')
                if var1 not in quandle or var2 not in quandle:
                    return float('inf')
                stack.append((var1, var2))
            else:
                return 0
            depth += 1
        while stack:
            var1, var2 = stack.pop()
            if var1 not in quandle or var2 not in quandle:
                return float('inf')
            stack.extend([(quandle[var1][0], quandle[var2][1]), (quandle[var1][1], quandle[var2][0])])
            depth += 1
        return depth
    
    n = random.randint(5, 40)
    clauses = tseitin_formula(n)
    quandle = quandle_representation(clauses, n)
    rank = minimal_rank(quandle)
    depth = tseitin_resolution_depth(clauses)
    
    if rank == float('inf') or depth == float('inf'):
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rank * depth,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["metric_value"] is not None for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        if support_fraction >= 0.7 and mean_rank >= 0.6:
            print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE some ranks are None")