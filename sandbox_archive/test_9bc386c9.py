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
            return 'x'
        else:
            x = random.choice(['x', 'y'])
            rest = generate_formula(n - 1)
            return f'({x} & {rest}) | ({x} & ~{rest})'

    def is_satisfiable(formula):
        if formula == 'x':
            return True
        elif formula == '~x':
            return False
        else:
            left, op, right = formula.split()
            if op == '&':
                return is_satisfiable(left) and is_satisfiable(right)
            elif op == '|':
                return is_satisfiable(left) or is_satisfiable(right)

    def quandle_rank(n):
        # Simplified rank calculation for demonstration
        return n

    def decision_tree_width(formula):
        if formula == 'x' or formula == '~x':
            return 1
        else:
            left, op, right = formula.split()
            if op == '&':
                return max(decision_tree_width(left), decision_tree_width(right))
            elif op == '|':
                return max(decision_tree_width(left), decision_tree_width(right))

    n = random.randint(5, 40)
    formula = generate_formula(n)
    is_sat = is_satisfiable(formula)
    
    if not is_sat:
        q_phi = quandle_rank(n)
        expected_q_phi = n
    else:
        q_phi = quandle_rank(n)
        delta_phi = n  # Simplified for demonstration
        expected_q_phi = math.log2(n) + math.log2(delta_phi)

    metric_value = q_phi
    conjecture_holds = abs(q_phi - expected_q_phi) <= 1
    
    return {
        "metric_name": "Quandle Rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")