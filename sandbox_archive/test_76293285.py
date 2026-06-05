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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x for x in clause}
            else:
                clause = {-x for x in clause}
            clauses.append(clause)
        return clauses
    
    def circuit_monotone_width(cnf):
        width = 0
        for clause in cnf:
            if all(abs(x) in assignment for x in clause):
                width += 1
        return width
    
    def minimal_grammar_complexity(cnf):
        grammar = {}
        for clause in cnf:
            for literal in clause:
                if literal not in grammar:
                    grammar[literal] = set()
                for other_literal in clause:
                    if other_literal != literal:
                        grammar[literal].add(other_literal)
        return len(grammar)
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            m = random.randint(1, min(n * (n - 1) // 2, 10))
            cnf = generate_cnf(m, n)
            width = circuit_monotone_width(cnf)
            complexity = minimal_grammar_complexity(cnf)
            instances_tested += 1
            total_metric_value += complexity / width
            n_max = max(n_max, n)
    
    metric_value = total_metric_value / instances_tested
    conjecture_holds = abs(metric_value - 1) < 0.5 and instances_tested >= 30
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "MinimalGrammarComplexity/WidthRatio",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")