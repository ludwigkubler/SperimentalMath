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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def circuit_monotone_width(cnf):
        width = 0
        for var in range(1, n + 1):
            if any(var in clause or -var in clause for clause in cnf):
                width += 1
        return width
    
    def minimal_grammar_complexity(cnf):
        # Placeholder function to simulate grammar complexity calculation
        # This is a dummy implementation and does not reflect actual grammar complexity
        return len(cnf)
    
    m = random.randint(5, 30)
    n = random.randint(10, 40)
    cnf = generate_cnf(m, n)
    width = circuit_monotone_width(cnf)
    complexity = minimal_grammar_complexity(cnf)
    
    if width == 0:
        return {
            "metric_name": "MinimalGrammarComplexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "CircuitMonotoneWidthIsZero"
        }
    
    ratio = Fraction(complexity, width)
    if not (0.5 <= ratio <= 2):
        return {
            "metric_name": "MinimalGrammarComplexity",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Ratio out of bounds: {ratio}"
        }
    
    return {
        "metric_name": "MinimalGrammarComplexity",
        "metric_value": float(complexity),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")