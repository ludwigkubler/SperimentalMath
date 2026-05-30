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
    
    def generate_sat_instance(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables + [f'~{v}' for v in variables], 3)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def compute_koszul_complex_size(instance):
        n = len(set(lit.split('~')[0] for lit in instance.split()))
        m = instance.count(' and ')
        if n == 0 or m == 0:
            return None
        return n * m
    
    def run_trial(seed: int) -> dict:
        random.seed(seed)
        
        def generate_sat_instance(n, m):
            variables = [f'x{i}' for i in range(1, n+1)]
            clauses = []
            for _ in range(m):
                clause = random.sample(variables + [f'~{v}' for v in variables], 3)
                clauses.append(' or '.join(clause))
            return ' and '.join(clauses)
        
        def compute_koszul_complex_size(instance):
            n = len(set(lit.split('~')[0] for lit in instance.split()))
            m = instance.count(' and ')
            if n == 0 or m == 0:
                return None
            return n * m
        
        instances_tested = 0
        total_generators = 0
        n_max = 1
        
        for n in [5, 10, 15, 20, 30, 40]:
            for _ in range(5):
                m = random.randint(n // 2, n * 2)
                instance = generate_sat_instance(n, m)
                generators = compute_koszul_complex_size(instance)
                if generators is not None:
                    instances_tested += 1
                    total_generators += generators
                    n_max = max(n_max, n)
        
        if instances_tested == 0:
            return {
                "metric_name": "Koszul Complex Generators",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": 1,
                "conjecture_holds": False,
                "counterexample": "No valid instances generated"
            }
        
        mean_generators = total_generators / instances_tested
        conjecture_bound = m**(2/3) * n_max**(1/6)
        ratio = mean_generators / conjecture_bound
        
        return {
            "metric_name": "Koszul Complex Generators",
            "metric_value": mean_generators,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": ratio <= 1.05,
            "counterexample": ""
        }
    
    trial_result = run_trial(seed)
    print(f"TRIAL: {trial_result}")
    
    return trial_result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    total_generators = 0
    instances_tested = 0
    n_max = 1
    
    for seed in seeds:
        trial_result = run_trial(seed)
        total_generators += trial_result["metric_value"] * trial_result["instances_tested"]
        instances_tested += trial_result["instances_tested"]
        n_max = max(n_max, trial_result["n_max"])
    
    if instances_tested == 0:
        print("RESULT: INCONCLUSIVE no valid instances generated")
    else:
        mean_generators = total_generators / instances_tested
        support_fraction = sum(1 for result in seeds if result["conjecture_holds"]) / len(seeds)
        
        if support_fraction >= 0.9:
            print(f"RESULT: SUPPORTED mean={mean_generators} std=NA support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed=NA")
        else:
            print("RESULT: INCONCLUSIVE insufficient support")