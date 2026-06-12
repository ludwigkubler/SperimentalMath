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
    
    def generate_boolean_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(random.randint(5, 20)):
            clause = random.sample(literals, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def construct_quandle(clauses):
        elements = set()
        for clause in clauses:
            for literal in clause:
                elements.add(literal)
        quandle = {e: e for e in elements}
        
        def operation(e1, e2):
            if e1 == e2:
                return e1
            elif e1 in quandle and e2 in quandle[e1]:
                return quandle[e1]
            else:
                return e2
        
        for clause in clauses:
            result = clause[0]
            for literal in clause[1:]:
                result = operation(result, literal)
            quandle[result] = result
            for literal in clause:
                if literal not in quandle or quandle[literal] != result:
                    quandle[literal] = result
        
        return quandle
    
    def minimal_quandle_rank(quandle):
        rank = 0
        seen = set()
        for e in quandle:
            if e not in seen:
                rank += 1
                stack = [e]
                while stack:
                    current = stack.pop()
                    if current not in seen:
                        seen.add(current)
                        for other in quandle:
                            if operation(current, other) == other and other not in seen:
                                stack.append(other)
        return rank
    
    def clause_tree_depth(clauses):
        depth = 0
        for clause in clauses:
            depth = max(depth, len(clause))
        return depth
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        formula = generate_boolean_formula(n)
        quandle = construct_quandle(formula)
        qrank = minimal_quandle_rank(quandle)
        ctdepth = clause_tree_depth(formula)
        
        metric_values.append(qrank * ctdepth)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((metric_values[i] - mean_value) * (i + 1 - instances_tested / 2) for i in range(len(metric_values))) / (len(metric_values) * std_value * math.sqrt(instances_tested ** 2 / 4 - 1))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "qrank * ctdepth",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")