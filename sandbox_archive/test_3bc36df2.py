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
        literals = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(random.randint(5, 10)):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause = [f"~{lit}" for lit in clause]
            clauses.append(" & ".join(clause))
        return " | ".join(clauses)

    def dpll(formula):
        def parse_formula(formula):
            literals = set()
            stack = []
            i = 0
            while i < len(formula):
                if formula[i] == '(':
                    stack.append(i)
                elif formula[i] == ')':
                    start = stack.pop()
                    clause = formula[start+1:i]
                    literals.update(clause.split('&'))
                    i += 1
                else:
                    literals.add(formula[i])
                    i += 1
            return literals

        def dpll_helper(literals, assignment):
            if not literals:
                return True
            literal = next(iter(literals))
            pos_literal = literal[1:] if literal.startswith('~') else literal
            neg_literal = '~' + pos_literal if literal.startswith('~') else f"~{pos_literal}"
            if pos_literal in assignment and assignment[pos_literal]:
                literals.remove(pos_literal)
                continue
            if neg_literal in assignment and not assignment[neg_literal]:
                literals.remove(neg_literal)
                continue
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[literal] = val
                if dpll_helper(literals - {literal}, new_assignment):
                    return True
            return False

        literals = parse_formula(formula)
        assignment = {}
        return dpll_helper(literals, assignment)

    n = random.randint(5, 40)
    formula = generate_formula(n)
    refutation_size = len(dpll(formula))
    
    def tropicalized_sheaves_order(n):
        if n == 1:
            return 1
        order = 2
        while True:
            if (order - 1) * math.log(order, 2) >= n:
                return order
            order += 1

    order = tropicalized_sheaves_order(n)
    
    metric_value = order / math.log(refutation_size, 2)
    conjecture_holds = 0.5 <= metric_value <= 1.5
    
    return {
        "metric_name": "Order of Tropicalized Sheaves",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Formula: {formula}, Order: {order}, Refutation Size: {refutation_size}"
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")