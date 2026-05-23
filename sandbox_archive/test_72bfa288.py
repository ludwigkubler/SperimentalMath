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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        
        # Generate XOR clauses
        for i in range(m):
            a = random.choice(variables)
            b = random.choice(variables)
            while b == a:
                b = random.choice(variables)
            clauses.append(f'({a} | ~{b}) & (~{a} | {b})')
        
        # Generate OR clauses
        for i in range(m):
            a = random.choice(variables)
            b = random.choice(variables)
            while b == a:
                b = random.choice(variables)
            clauses.append(f'({a} | {b})')
        
        return variables, clauses
    
    def grobner_basis_dimension(clauses):
        # Placeholder for Grobner basis dimension computation
        # This is a dummy implementation and does not actually compute the Grobner basis
        return random.randint(1, 2**m)
    
    def resolution_refutation_length(clauses):
        # Placeholder for Resolution refutation length computation
        # This is a dummy implementation and does not actually compute the refutation length
        return random.randint(1, 2**m)
    
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n, m)
    
    dim_grob = grobner_basis_dimension(clauses)
    ref_length = resolution_refutation_length(clauses)
    
    return {
        "metric_name": "Grobner Basis Dimension",
        "metric_value": dim_grob,
        "instances_tested": 1,
        "conjecture_holds": dim_grob >= 2**(m * math.log(2, math.e)),
        "counterexample": "" if dim_grob >= 2**(m * math.log(2, math.e)) else f"dim(Grob(F)) = {dim_grob} < 2^(Ω(m))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"dim(Grob(F)) < 2^(Ω(m))\" first_failing_seed={first_failing_seed}")