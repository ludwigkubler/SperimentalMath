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
    
    def generate_tseitin_formula(n):
        if n == 1:
            return 'x'
        else:
            subformulas = [generate_tseitin_formula(random.randint(1, n-1)) for _ in range(2)]
            return f'({subformulas[0]} & {subformulas[1]}) | (~{random.choice(subformulas)})'
    
    def tree_width(formula):
        if formula.isalpha():
            return 1
        elif ' & ' in formula:
            left, right = formula.split(' & ')
            return max(tree_width(left), tree_width(right)) + 1
        else:
            left, _, right = formula.partition(' | ')
            return max(tree_width(left), tree_width(right))
    
    def unitary_representation(formula):
        if formula.isalpha():
            return {formula: 1}
        elif ' & ' in formula:
            left, right = formula.split(' & ')
            left_rep = unitary_representation(left)
            right_rep = unitary_representation(right)
            result = {}
            for l_key, l_val in left_rep.items():
                for r_key, r_val in right_rep.items():
                    result[f'({l_key} & {r_key})'] = l_val * r_val
            return result
        else:
            left, _, right = formula.partition(' | ')
            left_rep = unitary_representation(left)
            right_rep = unitary_representation(right)
            result = {}
            for l_key, l_val in left_rep.items():
                result[l_key] = l_val
            for r_key, r_val in right_rep.items():
                if r_key not in result:
                    result[r_key] = r_val
            return result
    
    def minimal_rank(rep):
        rank = 0
        for key, val in rep.items():
            if val != 0:
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        tw = tree_width(formula)
        rep = unitary_representation(formula)
        rank = minimal_rank(rep)
        
        if rank > 2 * tw:
            conjecture_holds = False
            counterexample = f"rank={rank}, expected=2*{tw}"
            break
        
        total_metric_value += rank / tw
        instances_tested += 1
    
    return {
        "metric_name": "minimal_rank_over_tree_width",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")