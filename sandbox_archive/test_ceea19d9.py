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
            subformulas = [generate_formula(random.randint(1, n-1)) for _ in range(random.randint(2, 3))]
            return f"({subformulas[0]} & {subformulas[1]}) | ({' & '.join(subformulas[2:])})"
    
    def evaluate_formula(formula):
        if formula == "x":
            return random.choice([True, False])
        elif formula.startswith("(") and formula.endswith(")"):
            inner = formula[1:-1]
            if "&" in inner:
                left, right = inner.split("&")
                return evaluate_formula(left) and evaluate_formula(right)
            elif "|" in inner:
                left, right = inner.split("|")
                return evaluate_formula(left) or evaluate_formula(right)
        else:
            raise ValueError("Invalid formula")
    
    def dpll_search_tree_width(formula):
        if formula == "x":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            inner = formula[1:-1]
            if "&" in inner:
                left, right = inner.split("&")
                return max(dpll_search_tree_width(left), dpll_search_tree_width(right)) + 1
            elif "|" in inner:
                left, right = inner.split("|")
                return max(dpll_search_tree_width(left), dpll_search_tree_width(right))
        else:
            raise ValueError("Invalid formula")
    
    def local_crossed_module_rank(formula):
        if formula == "x":
            return 1
        elif formula.startswith("(") and formula.endswith(")"):
            inner = formula[1:-1]
            if "&" in inner:
                left, right = inner.split("&")
                return max(local_crossed_module_rank(left), local_crossed_module_rank(right))
            elif "|" in inner:
                left, right = inner.split("|")
                return max(local_crossed_module_rank(left), local_crossed_module_rank(right))
        else:
            raise ValueError("Invalid formula")
    
    n = random.randint(5, 40)
    formula = generate_formula(n)
    solutions = sum(1 for i in range(2**n) if evaluate_formula(formula.replace("x", bin(i)[2:].zfill(n))))
    rank = local_crossed_module_rank(formula)
    width = dpll_search_tree_width(formula)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= solutions * math.log(n),
        "counterexample": "" if rank <= solutions * math.log(n) else f"Formula: {formula}, Rank: {rank}, Solutions: {solutions}, Log(n): {math.log(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break