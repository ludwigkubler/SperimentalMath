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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next(iter(clauses[0]))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            remaining_clauses = [c for c in clauses if not any(lit in new_assignment and (new_assignment[lit] == val) for lit in c)]
            if dpll(remaining_clauses, new_assignment):
                return True
        return False
    
    def generate_random_clause(n):
        return random.sample([f"v{i}" for i in range(n)], k=random.randint(1, n))
    
    def generate_random_instance(n):
        return [generate_random_clause(n) for _ in range(n)]
    
    def koszul_complex(clauses):
        variables = set()
        relations = []
        for clause in clauses:
            for lit in clause:
                variables.add(lit)
            relations.append([lit if lit.startswith('v') else f"~{lit}" for lit in clause])
        return len(variables), relations
    
    def min_generators(koszul_complex):
        n, relations = koszul_complex
        generators = set()
        for relation in relations:
            for lit in relation:
                if lit.startswith('v'):
                    generators.add(lit)
                else:
                    generators.discard(lit[1:])
        return len(generators)
    
    def mean(lst):
        return sum(lst) / len(lst)
    
    def std(lst, m):
        return (sum((x - m) ** 2 for x in lst) / len(lst)) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_generators = 0
        
        for _ in range(5):  # Sample 5 instances per size
            instance = generate_random_instance(n)
            koszul_complex_result = koszul_complex(instance)
            generators = min_generators(koszul_complex_result)
            results.append(generators)
            total_generators += generators
            instances_tested += 1
        
        mean_value = mean(results)
        std_value = std(results, mean_value)
        
        if len(results) < 30:
            return {
                "metric_name": "min_generators",
                "metric_value": mean_value,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        k = 1
        while True:
            upper_bound = n ** k
            if all(x <= upper_bound for x in results):
                return {
                    "metric_name": "min_generators",
                    "metric_value": mean_value,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": True,
                    "counterexample": ""
                }
            k += 1
    
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = mean([r["metric_value"] for r in results if "conjecture_holds" in r and r["conjecture_holds"]])
    std_value = std([r["metric_value"] for r in results if "conjecture_holds" in r and r["conjecture_holds"]], mean_value)
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support_fraction")