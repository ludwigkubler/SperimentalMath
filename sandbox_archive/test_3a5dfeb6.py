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
    
    def generate_3cnf(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.choice([1, -1]) * i for i in range(1, n + 1)]
            random.shuffle(clause)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def frege_proof_depth(clauses):
        depth = 0
        stack = []
        for clause in clauses:
            if len(stack) == 0 or all(abs(x) not in [abs(y) for y in stack[-1]] for x in clause):
                stack.append([x for x in clause])
                depth += 1
            else:
                new_clause = []
                for x in clause:
                    if abs(x) in [abs(y) for y in stack[-1]]:
                        continue
                    new_clause.append(x)
                stack.pop()
                stack.append(new_clause)
                depth += 1
        return depth

    def coxeter_diagram(edges):
        diagram = {}
        for u, v in edges:
            if u not in diagram:
                diagram[u] = set()
            if v not in diagram:
                diagram[v] = set()
            diagram[u].add(v)
            diagram[v].add(u)
        return diagram

    def count_edges(diagram):
        return sum(len(neighbors) for neighbors in diagram.values()) // 2

    n_max = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        for _ in range(5):
            clauses = generate_3cnf(n, 0.5)
            depth = frege_proof_depth(clauses)
            if depth > n_max:
                n_max = depth
            edges = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    common_vars = set(abs(x) for x in clauses[i]) & set(abs(y) for y in clauses[j])
                    if common_vars:
                        edges.append((i, j))
            diagram = coxeter_diagram(edges)
            num_edges = count_edges(diagram)
            instances_tested += 1
            metric_values.append(num_edges)

    mean_value = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    conjecture_holds = all(x <= 10 for x in metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Number of distinct edges in Coxeter diagram",
        "metric_value": mean_value,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)

    mean_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev = math.sqrt(sum((x["metric_value"] - mean_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)

    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not x["conjecture_holds"] for x in results):
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")