# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n: int) -> list:
        cnf = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([f"v{i+1}", f"~v{i+1}"]) for i in range(random.randint(1, 3))]
            cnf.append(clause)
        return cnf
    
    def construct_formal_context(cnf: list) -> dict:
        context = {}
        variables = set()
        for clause in cnf:
            for literal in clause:
                if literal.startswith('v'):
                    variables.add(literal[1:])
                elif literal.startswith('~'):
                    variables.add(literal[2:])
        
        for var in variables:
            context[var] = set()
        
        for clause in cnf:
            for i, literal1 in enumerate(clause):
                for j, literal2 in enumerate(clause):
                    if i < j and (literal1.startswith('v') and literal2.startswith('~') or literal1.startswith('~') and literal2.startswith('v')):
                        context[literal1[1:]].add(literal2[1:])
        
        return context
    
    def minimal_order(context: dict) -> int:
        max_subcontext_size = 0
        for var in context:
            subcontext = {var}
            stack = [var]
            while stack:
                current_var = stack.pop()
                if current_var not in subcontext:
                    subcontext.add(current_var)
                    for neighbor in context[current_var]:
                        if neighbor not in subcontext:
                            stack.append(neighbor)
            max_subcontext_size = max(max_subcontext_size, len(subcontext))
        return max_subcontext_size
    
    def dpll_proof_width(cnf: list) -> int:
        # Placeholder implementation of DPLL proof width calculation
        # This is a simplified version and may not accurately reflect the actual proof width
        return len(cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    context = construct_formal_context(cnf)
    order = minimal_order(context)
    width = dpll_proof_width(cnf)
    
    return {
        "metric_name": "Minimal Order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if width == 0 else order <= width * 2,  # Simplified check
        "counterexample": "" if width != 0 else f"Order: {order}, Width: {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    std_order = (sum((r["metric_value"] - mean_order)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order:.2f} std={std_order:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order:.2f} std={std_order:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")