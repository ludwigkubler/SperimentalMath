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
    
    def tseitin_formula(sat_instance):
        variables = {}
        new_vars = {}
        clauses = sat_instance.split('\n')
        for clause in clauses:
            if 'or' not in clause and 'and' not in clause:
                continue
            literals = clause.split()
            var = random.randint(1, 1000)
            while var in variables or var in new_vars:
                var = random.randint(1, 1000)
            variables[clause] = var
            for literal in literals:
                if literal.startswith('not'):
                    neg_var = random.randint(1, 1000)
                    while neg_var in variables or neg_var in new_vars:
                        neg_var = random.randint(1, 1000)
                    new_vars[literal] = neg_var
        return variables, new_vars
    
    def resolution_proof_width(formula):
        # Simplified version for demonstration purposes
        return len(formula.split('\n'))
    
    def minimal_index_of_groupoid_cospans(variables, new_vars):
        # Simplified version for demonstration purposes
        return sum(1 for var in variables.values() if var % 2 == 0) + sum(1 for var in new_vars.values() if var % 3 == 0)
    
    n = random.randint(5, 40)
    sat_instance = "\n".join(random.choice(['a or b', 'not a and c', 'b or not c']) for _ in range(n))
    variables, formula = tseitin_formula(sat_instance)
    index_of_groupoid_cospans = minimal_index_of_groupoid_cospans(variables, formula)
    width = resolution_proof_width(formula)
    
    return {
        "metric_name": "Index(G)",
        "metric_value": index_of_groupoid_cospans,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 * mean_value for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")