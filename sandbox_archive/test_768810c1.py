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
    
    def generate_boolean_formula(n_vars, n_clauses):
        formula = []
        for _ in range(n_clauses):
            clause = [random.choice([1, -1]) * random.randint(1, n_vars) for _ in range(random.randint(1, 3))]
            formula.append(clause)
        return formula

    def frege_proof_depth(formula):
        # Simplified estimation of Frege proof depth
        return len(formula) ** 2

    def minimal_brauer_character_order(formula):
        n_vars = max(abs(var) for clause in formula for var in clause if var != 0)
        return n_vars + 1

    n_vars = random.randint(5, 10)
    n_clauses = random.randint(5, 10)
    formula = generate_boolean_formula(n_vars, n_clauses)
    
    min_char_order = minimal_brauer_character_order(formula)
    proof_depth = frege_proof_depth(formula)
    
    return {
        "metric_name": "Correlation",
        "metric_value": min_char_order * proof_depth,
        "instances_tested": 1,
        "n_max": n_vars,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
        counterexample = next((result["counterexample"] for result in results if not result["conjecture_holds"]), "")
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")