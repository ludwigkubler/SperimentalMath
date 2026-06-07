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
    
    def p_adic_valuation_rank(cnf):
        primes = [2]
        for i in range(3, 50, 2):
            if all(i % p != 0 for p in primes):
                primes.append(i)
        
        valrank = 0
        for clause in cnf:
            prime_ideals = set()
            for literal in clause:
                if literal > 0:
                    factor = literal
                else:
                    factor = -literal
                while factor % 2 == 0:
                    factor //= 2
                for p in primes:
                    if factor % p == 0 and p not in prime_ideals:
                        prime_ideals.add(p)
            valrank += len(prime_ideals)
        return valrank
    
    def dpll(cnf):
        def solve(model, clause_index=0):
            if clause_index == len(cnf):
                return True
            literals = cnf[clause_index]
            for literal in literals:
                if literal > 0 and literal not in model:
                    new_model = model | {literal: True}
                    if solve(new_model, clause_index + 1):
                        return True
                elif literal < 0 and -literal not in model:
                    new_model = model | {-literal: False}
                    if solve(new_model, clause_index + 1):
                        return True
            return False
        
        return solve({})
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2 ** n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
            cnf.append(clause)
        return cnf
    
    n_max = 0
    instances_tested = 0
    total_valrank = Fraction(0)
    total_dpl = Fraction(0)
    
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        valrank = p_adic_valuation_rank(cnf)
        dpl = dpll(cnf)
        
        total_valrank += Fraction(valrank)
        total_dpl += Fraction(dpl)
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_valrank = total_valrank / instances_tested
    mean_dpl = total_dpl / instances_tested
    
    correlation_coefficient = (instances_tested * sum(valrank * dpl for valrank, dpl in zip([mean_valrank] * instances_tested, [mean_dpl] * instances_tested)) -
                               sum(mean_valrank) * sum(mean_dpl)) / math.sqrt((instances_tested * sum(valrank ** 2 for valrank in [mean_valrank] * instances_tested) - sum(mean_valrank) ** 2) *
                                                                         (instances_tested * sum(dpl ** 2 for dpl in [mean_dpl] * instances_tested) - sum(mean_dpl) ** 2))
    
    conjecture_holds = correlation_coefficient > 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")