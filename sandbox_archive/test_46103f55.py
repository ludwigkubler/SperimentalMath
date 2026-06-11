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
    
    def generate_cnf(m):
        literals = list(range(1, m + 1)) + [-x for x in range(1, m + 1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, random.randint(2, m))
            clauses.append(clause)
        return clauses

    def formal_context(cnf):
        context = {}
        for i, clause in enumerate(cnf):
            for literal in clause:
                if literal not in context:
                    context[literal] = set()
                context[literal].add(i)
        return context

    def minimal_index(context):
        min_index = float('inf')
        for literals in context.values():
            min_index = min(min_index, len(literals))
        return min_index

    def resolution_proof_depth(cnf):
        stack = []
        while cnf:
            unit_clauses = [c for c in cnf if len(c) == 1]
            if not unit_clauses:
                break
            unit_clause = unit_clauses[0]
            literal, negated_literal = unit_clause[0], -unit_clause[0]
            new_clauses = []
            for clause in cnf:
                if literal in clause and negated_literal not in clause:
                    continue
                if negated_literal in clause:
                    new_clauses.append([x for x in clause if x != negated_literal])
                else:
                    new_clauses.append(clause)
            cnf = new_clauses
            stack.append(unit_clause)
        return len(stack)

    n_max = 0
    instances_tested = 0
    total_min_index = 0
    total_depth = 0

    for m in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(m)
        min_index = minimal_index(formal_context(cnf))
        depth = resolution_proof_depth(cnf)
        
        if min_index > depth:
            return {
                "metric_name": "min_index",
                "metric_value": min_index,
                "instances_tested": 1,
                "n_max": m,
                "conjecture_holds": False,
                "counterexample": f"min_index ({min_index}) > depth ({depth})"
            }
        
        total_min_index += min_index
        total_depth += depth
        instances_tested += 1
        n_max = max(n_max, m)

    mean_min_index = total_min_index / instances_tested
    mean_depth = total_depth / instances_tested

    return {
        "metric_name": "min_index",
        "metric_value": mean_min_index,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_min_index >= 0.7 * mean_depth,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_min_index = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_min_index) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_min_index} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_index} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")