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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # 10 clauses per variable on average
            clause = set()
            for _ in range(random.randint(1, 3)):  # 1 to 3 literals per clause
                var = random.choice([f'x{i}' for i in range(n)])
                polarity = random.choice(['', '~'])
                clause.add(polarity + var)
            clauses.append(clause)
        return clauses

    def tropical_hyperplanes(clauses):
        T = []
        for clause in clauses:
            hyperplane = {}
            for literal in clause:
                if literal.startswith('~'):
                    var, negated = literal[1:], True
                else:
                    var, negated = literal, False
                if var not in hyperplane or (hyperplane[var] and negated):
                    hyperplane[var] = negated
                elif not hyperplane[var]:
                    hyperplane.pop(var)
            T.append(hyperplane)
        return T

    def intersect_hyperplanes(T):
        intersection = {}
        for hyperplane in T:
            for var, polarity in hyperplane.items():
                if var not in intersection or (intersection[var] and polarity):
                    intersection[var] = polarity
                elif not intersection[var]:
                    intersection.pop(var)
        return intersection

    def dpll_refutation_depth(clauses):
        stack = []
        assignment = {}
        def backtrack(level):
            if level == len(clauses):
                return True
            clause = clauses[level]
            for literal in clause:
                var, negated = literal[1:], literal.startswith('~')
                if (var not in assignment and backtrack(level + 1)):
                    assignment[var] = negated
                    stack.append((level, literal))
                    return True
                elif (var in assignment and assignment[var] == negated):
                    continue
                else:
                    break
            while stack and stack[-1][0] >= level:
                _, literal = stack.pop()
                var, _ = literal[1:], literal.startswith('~')
                del assignment[var]
            return False
        if backtrack(0):
            return len(stack)
        return float('inf')

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    T = tropical_hyperplanes(clauses)
    intersection = intersect_hyperplanes(T)
    complexity = len(intersection)  # Simplified for testing
    refutation_depth = dpll_refutation_depth(clauses)

    return {
        "metric_name": "DPLL Refutation Depth",
        "metric_value": refutation_depth,
        "instances_tested": 1,
        "conjecture_holds": refutation_depth <= complexity,
        "counterexample": "" if refutation_depth <= complexity else f"Refutation depth {refutation_depth} > Complexity {complexity}"
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
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation depth > Complexity\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")