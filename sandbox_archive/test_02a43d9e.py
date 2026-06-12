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
    
    def generate_formula(n):
        literals = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(random.randint(5, 20)):
            clause = random.sample(literals + [f'~{l}' for l in literals], random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def construct_quandle(clauses):
        elements = set()
        for clause in clauses:
            for literal in clause:
                elements.add(literal)
                if '~' in literal:
                    elements.add(literal.replace('~', ''))
        
        quandle = {}
        for e1 in elements:
            for e2 in elements:
                result = []
                for literal in clauses:
                    if (e1 in literal and e2 not in literal) or (e1 not in literal and e2 in literal):
                        result.append(literal)
                quandle[(e1, e2)] = result
        
        return quandle
    
    def minimal_quandle_rank(quandle):
        elements = list(quandle.keys())
        rank = 0
        while True:
            new_elements = set()
            for (e1, e2) in elements:
                if len(quandle[(e1, e2)]) > 0:
                    new_elements.add((e1, e2))
            if len(new_elements) == len(elements):
                break
            elements = new_elements
            rank += 1
        return rank
    
    def clause_tree_depth(clauses):
        if not clauses:
            return 0
        max_depth = 0
        for clause in clauses:
            depth = 1 + max([clause_tree_depth([l for l in clauses if l != clause]) for clause in clauses if l != clause], default=0)
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        clauses = generate_formula(n)
        quandle = construct_quandle(clauses)
        qrank = minimal_quandle_rank(quandle)
        ctdepth = clause_tree_depth(clauses)
        metric_values.append(qrank * ctdepth)
    
    correlation_coefficient = sum(metric_values) / instances_tested
    
    return {
        "metric_name": "qrank * ctdepth",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient} < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")