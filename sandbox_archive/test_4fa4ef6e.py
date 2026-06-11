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
    
    def generate_cnf(m: int, n: int):
        clauses = []
        for _ in range(m):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(1, n+1)]
            clause = ' OR '.join(literals)
            clauses.append(clause)
        return ' AND '.join(clauses)

    def formal_context(cnf: str, n: int):
        context = [[0] * n for _ in range(n)]
        literals = set()
        for clause in cnf.split(' AND '):
            for literal in clause.split(' OR '):
                if literal.startswith('x'):
                    literals.add(int(literal[1:]) - 1)
                elif literal.startswith('-x'):
                    literals.add(-int(literal[2:]) - 1)
        
        for i in range(n):
            for j in range(i, n):
                if (i in literals and j not in literals) or (j in literals and i not in literals):
                    context[i][j] = 1
                    context[j][i] = 1
        
        return context

    def min_index(context: list):
        rows, cols = len(context), len(context[0])
        visited = set()
        
        def dfs(r, c):
            if (r, c) in visited:
                return 0
            visited.add((r, c))
            count = 1
            for i in range(rows):
                if context[r][i] == 1 and i != r:
                    count += dfs(i, c)
            for j in range(cols):
                if context[j][c] == 1 and j != c:
                    count += dfs(r, j)
            return count
        
        max_index = 0
        for i in range(rows):
            for j in range(cols):
                if (i, j) not in visited:
                    index = dfs(i, j)
                    max_index = max(max_index, index)
        
        return max_index

    def resolution_depth(cnf: str):
        stack = [cnf]
        depth = 0
        
        while stack:
            current = stack.pop()
            if ' OR ' not in current:
                continue
            parts = current.split(' AND ')
            for part in parts:
                if ' OR ' in part:
                    literals = part.split(' OR ')
                    new_clause = ' AND '.join(literals)
                    stack.append(new_clause)
                    depth += 1
        
        return depth

    n = random.randint(5, 40)
    m = random.randint(1, min(n * (n - 1) // 2, 40))
    cnf = generate_cnf(m, n)
    
    context = formal_context(cnf, n)
    min_index_value = min_index(context)
    depth_value = resolution_depth(cnf)
    
    if min_index_value > depth_value:
        return {
            "metric_name": "min_index",
            "metric_value": min_index_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"min_index ({min_index_value}) > depth ({depth_value})"
        }
    
    return {
        "metric_name": "min_index",
        "metric_value": min_index_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = Fraction(len([r for r in results if r["conjecture_holds"]]), len(results)).limit_denominator()
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"min_index > depth\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")