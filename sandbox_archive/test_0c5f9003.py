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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def lidb(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        def truth_table_to_formula(tt):
            if len(tt) == 1:
                return str(tt[0])
            mid = len(tt) // 2
            left = truth_table_to_formula(tt[:mid])
            right = truth_table_to_formula(tt[mid:])
            return f"({left} & {right})"
        
        def simplify(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                if left == '0' or right == '0':
                    return '0'
                elif left == '1':
                    return right
                elif right == '1':
                    return left
                else:
                    return f"({left} & {right})"
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                if left == '1' or right == '1':
                    return '1'
                elif left == '0':
                    return right
                elif right == '0':
                    return left
                else:
                    return f"({left} | {right})"
            return formula
        
        def evaluate(formula, assignment):
            if isinstance(formula, int):
                return formula
            elif formula in '01':
                return int(formula)
            elif ' & ' in formula:
                left, right = formula.split(' & ')
                return evaluate(left, assignment) and evaluate(right, assignment)
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                return evaluate(left, assignment) or evaluate(right, assignment)
        
        def truth_table_to_formula(tt):
            if len(tt) == 1:
                return str(tt[0])
            mid = len(tt) // 2
            left = truth_table_to_formula(tt[:mid])
            right = truth_table_to_formula(tt[mid:])
            return f"({left} & {right})"
        
        def simplify(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                if left == '0' or right == '0':
                    return '0'
                elif left == '1':
                    return right
                elif right == '1':
                    return left
                else:
                    return f"({left} & {right})"
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                if left == '1' or right == '1':
                    return '1'
                elif left == '0':
                    return right
                elif right == '0':
                    return left
                else:
                    return f"({left} | {right})"
        
        def evaluate(formula, assignment):
            if isinstance(formula, int):
                return formula
            elif formula in '01':
                return int(formula)
            elif ' & ' in formula:
                left, right = formula.split(' & ')
                return evaluate(left, assignment) and evaluate(right, assignment)
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                return evaluate(left, assignment) or evaluate(right, assignment)
        
        tt = f[:]
        while len(tt) > 1:
            new_tt = []
            for i in range(len(tt) // 2):
                new_tt.append(evaluate(truth_table_to_formula(tt[2*i:2*(i+1)]), [0]))
                new_tt.append(evaluate(truth_table_to_formula(tt[2*i:2*(i+1)]), [1]))
            tt = new_tt
        return len(simplify(truth_table_to_formula(f)))
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Input must be a Boolean function with 2^n values")
        
        def truth_table_to_formula(tt):
            if len(tt) == 1:
                return str(tt[0])
            mid = len(tt) // 2
            left = truth_table_to_formula(tt[:mid])
            right = truth_table_to_formula(tt[mid:])
            return f"({left} & {right})"
        
        def simplify(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                if left == '0' or right == '0':
                    return '0'
                elif left == '1':
                    return right
                elif right == '1':
                    return left
                else:
                    return f"({left} & {right})"
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                if left == '1' or right == '1':
                    return '1'
                elif left == '0':
                    return right
                elif right == '0':
                    return left
                else:
                    return f"({left} | {right})"
        
        def evaluate(formula, assignment):
            if isinstance(formula, int):
                return formula
            elif formula in '01':
                return int(formula)
            elif ' & ' in formula:
                left, right = formula.split(' & ')
                return evaluate(left, assignment) and evaluate(right, assignment)
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                return evaluate(left, assignment) or evaluate(right, assignment)
        
        def truth_table_to_formula(tt):
            if len(tt) == 1:
                return str(tt[0])
            mid = len(tt) // 2
            left = truth_table_to_formula(tt[:mid])
            right = truth_table_to_formula(tt[mid:])
            return f"({left} & {right})"
        
        def simplify(formula):
            if formula.startswith('(') and formula.endswith(')'):
                formula = formula[1:-1]
            if ' & ' in formula:
                left, right = formula.split(' & ')
                if left == '0' or right == '0':
                    return '0'
                elif left == '1':
                    return right
                elif right == '1':
                    return left
                else:
                    return f"({left} & {right})"
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                if left == '1' or right == '1':
                    return '1'
                elif left == '0':
                    return right
                elif right == '0':
                    return left
                else:
                    return f"({left} | {right})"
        
        def evaluate(formula, assignment):
            if isinstance(formula, int):
                return formula
            elif formula in '01':
                return int(formula)
            elif ' & ' in formula:
                left, right = formula.split(' & ')
                return evaluate(left, assignment) and evaluate(right, assignment)
            elif ' | ' in formula:
                left, right = formula.split(' | ')
                return evaluate(left, assignment) or evaluate(right, assignment)
        
        tt = f[:]
        while len(tt) > 1:
            new_tt = []
            for i in range(len(tt) // 2):
                new_tt.append(evaluate(truth_table_to_formula(tt[2*i:2*(i+1)]), [0]))
                new_tt.append(evaluate(truth_table_to_formula(tt[2*i:2*(i+1)]), [1]))
            tt = new_tt
        return len(simplify(truth_table_to_formula(f)))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            lidb_value = lidb(f)
            comm_rank_variance = communication_complexity_rank_variance(f)
            results.append((lidb_value, comm_rank_variance))
    
    if len(results) < 30 * len(n_values):
        return {
            "metric_name": "LIDB vs CommRankVar",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    lidb_values = [r[0] for r in results]
    comm_rank_variances = [r[1] for r in results]
    
    mean_lidb = sum(lidb_values) / len(lidb_values)
    mean_comm_rank_variance = sum(comm_rank_variances) / len(comm_rank_variances)
    mean_diff = abs(mean_lidb - mean_comm_rank_variance)
    
    correlation_coefficient = 0
    if len(lidb_values) > 1:
        numerator = sum((lidb_values[i] - mean_lidb) * (comm_rank_variances[i] - mean_comm_rank_variance) for i in range(len(lidb_values)))
        denominator = math.sqrt(sum((lidb_values[i] - mean_lidb)**2 for i in range(len(lidb_values))) * sum((comm_rank_variances[i] - mean_comm_rank_variance)**2 for i in range(len(comm_rank_variances))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "LIDB vs CommRankVar",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_metric_value = None
        std_metric_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] or r["counterexample"] != "" for r in results):
        counterexample = next((r["counterexample"] for r in results if r["counterexample"]), "")
        RESULT = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}"
    elif all(r["conjecture_holds"] for r in results):
        RESULT = f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}"
    else:
        RESULT = f"RESULT: INCONCLUSIVE reason=not_enough_support"
    
    print(RESULT)