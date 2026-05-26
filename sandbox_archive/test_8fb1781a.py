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
    
    def generate_random_graph(n):
        if n <= 0 or n > 40:
            return None
        graph = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            graph[i][i] = 0
        return graph
    
    def tseitin_formula(graph):
        if not graph:
            return []
        n = len(graph)
        clauses = []
        literals = {}
        var_id = 1
        
        def add_clause(clause):
            clauses.append(clause)
        
        for i in range(n):
            literals[(i, j)] = var_id
            var_id += 1
            add_clause([literals[(i, j)], literals[(j, i)]])
        
        for i in range(n):
            for j in range(n):
                if graph[i][j] == 1:
                    add_clause([-literals[(i, j)], -literals[(j, i)]])
        
        return clauses
    
    def resolution_refutation(clauses):
        def simplify(clause):
            return [x for x in clause if x != -x]
        
        def resolve(clause1, clause2):
            resolved = []
            for x in clause1:
                if -x in clause2:
                    continue
                resolved.append(x)
            return resolved
        
        queue = clauses[:]
        while True:
            new_clauses = set()
            changed = False
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    common = [x for x in queue[i] if -x in queue[j]]
                    if common:
                        resolvent = resolve(queue[i], queue[j])
                        new_clauses.add(tuple(sorted(resolvent)))
                        changed = True
            if not changed:
                break
            queue.extend(new_clauses)
        
        return len(queue)
    
    def graphical_virtual_knot_rank(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if graph[i][j] == 1:
                    rank += 1
        return rank
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    if not graph:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    tseitin_clauses = tseitin_formula(graph)
    resolution_length = resolution_refutation(tseitin_clauses)
    knot_rank = graphical_virtual_knot_rank(graph)
    
    return {
        "metric_name": "rank",
        "metric_value": knot_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(knot_rank - resolution_length) <= 2 * len(tseitin_clauses),
        "counterexample": "" if abs(knot_rank - resolution_length) <= 2 * len(tseitin_clauses) else f"rank={knot_rank}, expected={resolution_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")