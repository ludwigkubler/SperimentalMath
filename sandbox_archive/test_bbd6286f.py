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
    
    # Generate a random group and its representation V over a field F
    n = 5 + (seed % 40) // 8  # Sweep n through {5, 10, 15, 20, 30, 40}
    G = generate_group(n)
    V = generate_representation(G, seed)
    
    # Calculate the minimal rank of V
    minrank_V = calculate_minimal_rank(V)
    
    # Generate a k-CNF formula representing the boolean function encoded by V
    formula = generate_kcnf_formula(V, n)
    
    # Calculate the DPLL search tree width of the formula
    dpll_width = calculate_dpll_search_tree_width(formula)
    
    # Check if the conjecture holds for this seed
    c = 0.1  # Example constant, replace with actual value if known
    ratio = minrank_V / dpll_width
    conjecture_holds = ratio >= c
    
    return {
        "metric_name": "minrank(V) / DPLL_search_tree_width(G)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} < {c}"
    }

def generate_group(n: int) -> list:
    # Simple cyclic group G = Z/nZ
    return [i % n for i in range(n)]

def generate_representation(G: list, seed: int) -> list:
    # Random representation V of G over a field F (e.g., complex numbers)
    random.seed(seed + 1)
    dim = len(G)
    V = [[random.uniform(-1, 1) + random.uniform(-1, 1) * 1j for _ in range(dim)] for _ in range(dim)]
    return V

def calculate_minimal_rank(V: list) -> int:
    # Minimal rank of a matrix (number of non-zero singular values)
    n = len(V)
    U, _, Vh = svd(V)
    return sum(abs(s) > 1e-6 for s in Vh[0])

def generate_kcnf_formula(V: list, n: int) -> str:
    # Generate a random k-CNF formula representing the boolean function encoded by V
    k = 3  # Example clause length, replace with actual value if known
    num_clauses = n * n
    clauses = []
    for i in range(num_clauses):
        clause = [random.choice([f"x{i*n+j}", f"~x{i*n+j}"]) for j in range(k)]
        clauses.append(clause)
    return " & ".join(" | ".join(c) for c in clauses)

def calculate_dpll_search_tree_width(formula: str) -> int:
    # Simplified DPLL search tree width calculation (example implementation)
    stack = []
    for clause in formula.split(' & '):
        if not stack or all(abs(stack[-1][i]) < 1e-6 for i in clause):
            stack.append([int(c[2:]) if c.startswith('x') else -int(c[3:]) for c in clause])
    return len(stack)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")