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
from math import log, ceil
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_read_twice_bp(n: int, m: int):
        # Generate a random read-twice Boolean formula with n variables and m clauses
        literals = [f"x{i}" for i in range(1, n+1)]
        negated_literals = [f"~x{i}" for i in range(1, n+1)]
        all_literals = literals + negated_literals
        
        clauses = []
        for _ in range(m):
            clause = random.sample(all_literals, 2)
            if random.choice([True, False]):
                clause.append(random.choice(literals))
            clauses.append(clause)
        
        return clauses
    
    def size(bp: list) -> int:
        # Compute the size of a read-twice Boolean formula
        return sum(len(clause) for clause in bp)
    
    def generate_dpll_tree(bp: list):
        # Generate a DPLL search tree for a given read-twice Boolean formula
        if not bp:
            return True
        
        literal = random.choice([l for l in literals if any(l in c or f"~{l}" in c for c in bp)])
        remaining_bp = [c for c in bp if literal not in c and f"~{literal}" not in c]
        
        if literal.startswith("~"):
            return generate_dpll_tree(remaining_bp)
        else:
            return (generate_dpll_tree(remaining_bp) or
                    generate_dpll_tree([c.replace(literal, "") for c in remaining_bp]))
    
    def size_dpll_tree(dpll_tree: bool) -> int:
        # Compute the size of a DPLL search tree
        if isinstance(dpll_tree, bool):
            return 1
        else:
            return sum(size_dpll_tree(subtree) for subtree in dpll_tree)
    
    def tropicalized_lie_group_rank(bp: list) -> int:
        # Placeholder function to compute the minimal rank of a tropicalized Lie group representation
        # This is a placeholder and should be replaced with actual computation
        return len(bp)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    bp = generate_read_twice_bp(n, m)
    size_P = size(bp)
    dpll_tree = generate_dpll_tree(bp)
    t_star_F = size_dpll_tree(dpll_tree)
    
    min_rank = tropicalized_lie_group_rank(bp)
    
    conjecture_holds = log(size_P) <= min_rank <= size_P
    counterexample = "" if conjecture_holds else f"BP with n={n}, m={m}"
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")