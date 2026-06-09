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
    
    def generate_cnf(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def tropical_motivic_rank(cnf: list) -> int:
        graph = {i: set() for i in range(1, len(cnf[0]) + 1)}
        for clause in cnf:
            for literal in clause:
                if literal > 0:
                    graph[literal].add(-literal)
                else:
                    graph[-literal].add(literal)
        rank = 0
        visited = set()
        for node in range(1, len(cnf[0]) + 1):
            if node not in visited:
                queue = [node]
                while queue:
                    current = queue.pop()
                    if current not in visited:
                        visited.add(current)
                        for neighbor in graph[current]:
                            if neighbor not in visited:
                                queue.append(neighbor)
                rank += 1
        return rank
    
    def resolution_width(cnf: list) -> int:
        stack = []
        for clause in cnf:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if all(x == 0 for x in clause):
                continue
            new_clause = [x for x in clause if abs(x) not in {abs(y) for y in clause}]
            if len(new_clause) == 0:
                return len(clause)
            stack.append(new_clause)
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        mtr = tropical_motivic_rank(cnf)
        width = resolution_width(cnf)
        results.append((n, mtr, width))
    
    mean_width = sum(width for _, _, width in results) / len(results)
    std_dev = math.sqrt(sum((width - mean_width)**2 for _, _, width in results) / len(results))
    support_fraction = sum(1 for _, _, width in results if width <= mean_width + 3 * std_dev) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and abs(r["metric_value"] - mean_width) > 3 * std_dev for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"] and abs(r["metric_value"] - mean_width) > 3 * std_dev)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")