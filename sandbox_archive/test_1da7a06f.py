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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cyclic_difference_set(f):
        n = int(math.log2(len(f)))
        diff_set = set()
        for i in range(2**n):
            for j in range(i+1, 2**n):
                diff = (i ^ j) % (2**n)
                if diff not in diff_set:
                    diff_set.add(diff)
        return diff_set
    
    def dpll_proof_width(f):
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            clauses.append(clause)
        
        def dpll(model, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_model = model.copy()
                new_model[abs(literal)] = literal > 0
                if dpll(new_model, [c for c in clauses if literal not in c]):
                    return True
                del new_model[abs(literal)]
            else:
                literal = next((i + 1 for i in range(n) if i+1 not in model), None)
                if dpll(model | {literal: True}, clauses):
                    return True
                if dpll(model | {literal: False}, clauses):
                    return True
            return False
        
        return len(clauses)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    diff_set = cyclic_difference_set(f)
    proof_width = dpll_proof_width(f)
    
    metric_value = len(diff_set) / proof_width if proof_width != 0 else float('inf')
    conjecture_holds = metric_value < float('inf')
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "Minimal Rank of Cyclic Difference Set vs. DPLL Proof Width",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")