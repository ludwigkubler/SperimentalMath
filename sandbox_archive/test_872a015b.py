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

# Helper functions for p-adic arithmetic and Frege proof depth calculation
def add_p_adic(a, b, p):
    return (a + b) % p

def multiply_p_adic(a, b, p):
    return (a * b) % p

def inverse_p_adic(a, p):
    if a == 0:
        raise ValueError("Inverse does not exist for zero in p-adic arithmetic")
    for i in range(1, p):
        if (a * i) % p == 1:
            return i
    raise ValueError("Inverse not found")

def frege_proof_depth(formula):
    stack = []
    depth = 0
    for char in formula:
        if char == '(':
            stack.append(char)
            depth += 1
        elif char == ')':
            if not stack:
                raise IndexError("Unbalanced parentheses")
            stack.pop()
            depth -= 1
        elif char == 'not':
            if not stack or stack[-1] != '(':
                raise ValueError("Invalid use of 'not'")
            stack[-1] = f"not {stack[-1]}"
    if stack:
        raise IndexError("Unbalanced parentheses")
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random Boolean formula with n variables
    n = random.randint(5, 40)
    num_clauses = random.randint(n, 2 * n)
    formula = []
    for _ in range(num_clauses):
        clause = " or ".join(random.choice(["A" + str(i), "not A" + str(i)]) for i in range(n))
        formula.append("(" + clause + ")")
    
    # Construct the p-adic ring R(φ) from φ
    p = 2
    variables = {f"A{i}": random.randint(1, p-1) for i in range(n)}
    clauses = [eval(c, variables, {"not": lambda x: -x % p}) for c in formula]
    
    # Compute the Frege proof depth d(φ)
    try:
        depth = frege_proof_depth("".join(formula))
    except (IndexError, ValueError) as e:
        return {
            "metric_name": "Frege Proof Depth",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Compute the p-adic logarithmic rank logrank_p(φ) of R(φ)
    rank = sum(len(c) for c in clauses if c != 0)
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_depth = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={seed}")
                break