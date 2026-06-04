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
    
    def generate_boolean_instance(n):
        return [random.choice([-1, 1]) for _ in range(n)]
    
    def dpll(instance):
        if not instance:
            return True
        literal = next((lit for lit in instance if lit != -lit), None)
        if literal is None:
            return False
        new_instance = [x for x in instance if x != literal]
        if dpll(new_instance):
            return True
        new_instance = [x for x in instance if x != -literal]
        return dpll(new_instance)
    
    def find_monomial_generators(instance):
        n = len(instance)
        monomials = set()
        for i in range(1 << n):
            monomial = 1
            for j in range(n):
                if (i >> j) & 1:
                    monomial *= instance[j]
            monomials.add(monomial)
        return monomials
    
    def calculate_dpll_proof_length(instance):
        stack = [instance]
        length = 0
        while stack:
            instance = stack.pop()
            literal = next((lit for lit in instance if lit != -lit), None)
            if literal is None:
                break
            new_instance = [x for x in instance if x != literal]
            stack.append(new_instance)
            new_instance = [x for x in instance if x != -literal]
            stack.append(new_instance)
            length += 1
        return length
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = generate_boolean_instance(n)
        monomials = find_monomial_generators(instance)
        dpll_length = calculate_dpll_proof_length(instance)
        metric_values.append(len(monomials))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(0.5 * dpll_length <= len(monomials) <= 2 * dpll_length for monomials, dpll_length in zip(monomial_generators, dpll_lengths))
    
    return {
        "metric_name": "monomial_generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient=0' first_failing_seed={first_failing_seed}")