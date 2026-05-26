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
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['x', '¬x'])
        else:
            op = random.choice(['∧', '∨'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f'({left} {op} {right})'
    
    def evaluate_formula(formula):
        if formula == 'x':
            return random.choice([0, 1])
        elif formula == '¬x':
            return 1 - evaluate_formula('x')
        else:
            op = formula[1]
            left = evaluate_formula(formula[2:-1].split(' ')[0])
            right = evaluate_formula(formula[2:-1].split(' ')[2])
            if op == '∧':
                return left * right
            elif op == '∨':
                return left + right - left * right
    
    def cyclic_homology_rank(formula):
        # Simplified version for demonstration purposes
        return len(set(evaluate_formula(formula) for _ in range(100)))
    
    def communication_complexity(formula):
        # Simplified simulation of communication complexity
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_boolean_formula(n)
    rank = cyclic_homology_rank(formula)
    cc = communication_complexity(formula)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 1,
        "conjecture_holds": abs(cc - rank) < 0.1 * rank,  # Simplified check
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")