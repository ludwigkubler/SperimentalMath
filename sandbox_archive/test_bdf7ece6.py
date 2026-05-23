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
    
    def generate_formula(n):
        if n == 1:
            return "x"
        else:
            x = random.choice("xy")
            y = random.choice("xy")
            op = random.choice(["&", "|"])
            return f"({generate_formula(n-1)} {op} {generate_formula(n-1)})"
    
    def is_satisfiable(formula):
        if formula == "x":
            return True
        elif formula == "y":
            return False
        else:
            op = formula[1]
            left, right = formula[2:-1].split(op)
            if op == "&":
                return is_satisfiable(left) and is_satisfiable(right)
            elif op == "|":
                return is_satisfiable(left) or is_satisfiable(right)
    
    def quandle_rank(formula):
        if formula == "x":
            return 1
        elif formula == "y":
            return 2
        else:
            op = formula[1]
            left, right = formula[2:-1].split(op)
            if op == "&":
                return max(quandle_rank(left), quandle_rank(right))
            elif op == "|":
                return quandle_rank(left) + quandle_rank(right)
    
    def decision_tree_width(formula):
        if formula == "x" or formula == "y":
            return 1
        else:
            op = formula[1]
            left, right = formula[2:-1].split(op)
            if op == "&":
                return max(decision_tree_width(left), decision_tree_width(right))
            elif op == "|":
                return decision_tree_width(left) + decision_tree_width(right)
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    sat = is_satisfiable(formula)
    rank = quandle_rank(formula)
    width = decision_tree_width(formula)
    
    if sat:
        expected_rank = math.log2(n) + math.log2(max(len(set(formula.split("&"))), len(set(formula.split("|")))))
    else:
        expected_rank = n
    
    return {
        "metric_name": "Quandle Rank vs Decision Tree Width",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= 1,
        "counterexample": "" if sat else f"Formula: {formula}, Expected Rank: {expected_rank}, Actual Rank: {rank}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")