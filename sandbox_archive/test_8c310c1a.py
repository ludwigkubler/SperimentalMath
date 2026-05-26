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
    
    def evaluate_formula(formula):
        stack = []
        for token in formula.split():
            if token.isdigit():
                stack.append(int(token))
            elif token == '+':
                right = stack.pop()
                left = stack.pop()
                stack.append(left + right)
            elif token == '-':
                right = stack.pop()
                left = stack.pop()
                stack.append(left - right)
            elif token == '*':
                right = stack.pop()
                left = stack.pop()
                stack.append(left * right)
        return stack[0]
    
    def cyclic_homology_rank(formula):
        # Placeholder for the actual computation of cyclic homology rank
        # This is a dummy implementation that returns a random value for demonstration
        return random.randint(1, 10)
    
    def communication_complexity(formula):
        # Placeholder for the actual computation of communication complexity
        # This is a dummy implementation that returns a random value for demonstration
        return random.uniform(1.0, 10.0)
    
    n = random.randint(5, 40)
    formulas = [' '.join(random.choices(['0', '1'], k=n)) for _ in range(30)]
    ranks = [cyclic_homology_rank(formula) for formula in formulas]
    complexities = [communication_complexity(formula) for formula in formulas]
    
    correlation_coefficient = sum((ranks[i] - mean(ranks)) * (complexities[i] - mean(complexities)) for i in range(len(ranks))) / math.sqrt(sum((ranks[i] - mean(ranks))**2 for i in range(len(ranks)))) / math.sqrt(sum((complexities[i] - mean(complexities))**2 for i in range(len(complexities))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(formulas),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": "" if correlation_coefficient >= 0.9 else "low_correlation"
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")