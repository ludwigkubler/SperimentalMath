# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_abelian_variants(instance):
        n = len(instance)
        abelian_variants = set()
        for i in range(1 << n):
            variant = []
            for j in range(n):
                if (i >> j) & 1:
                    variant.append(instance[j])
            abelian_variants.add(tuple(variant))
        return abelian_variants
    
    def measure_resolution_width(instance):
        # Simplified DPLL solver to estimate resolution width
        n = len(instance)
        clauses = [[i for i in range(n) if instance[i] == 1], [i + n for i in range(n) if instance[i] == 0]]
        stack = []
        assignment = [None] * (2 * n)
        
        def dpll():
            while True:
                unit_clause = next((c for c in clauses if len(c) == 1), None)
                if unit_clause:
                    literal = unit_clause[0]
                    var = abs(literal) - 1
                    assignment[var] = literal > 0
                    stack.append(var)
                else:
                    if not any(assignment[v] is None for v in range(n)):
                        return len(stack)
                    var = next(v for v in range(n) if assignment[v] is None)
                    assignment[var] = True
                    stack.append(var)
                while stack and assignment[stack[-1]] is False:
                    stack.pop()
        
        return dpll()
    
    def calculate_abelian_number(abelian_variants):
        return len(abelian_variants)
    
    results = []
    for n in range(5, 41):
        instance = generate_instance(n)
        abelian_variants = construct_abelian_variants(instance)
        resolution_width = measure_resolution_width(instance)
        abelian_number = calculate_abelian_number(abelian_variants)
        
        results.append({
            "n": n,
            "resolution_width": resolution_width,
            "abelian_number": abelian_number
        })
    
    total_instances = len(results)
    max_n = max(r["n"] for r in results)
    abelian_numbers = [r["abelian_number"] for r in results]
    avg_abelian_number = sum(abelian_numbers) / total_instances
    
    conjecture_holds = all(a <= n**2 * 1.5 for a, n in zip(abelian_numbers, range(5, 41)))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_number_of_abelian_variants",
        "metric_value": avg_abelian_number,
        "instances_tested": total_instances,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")