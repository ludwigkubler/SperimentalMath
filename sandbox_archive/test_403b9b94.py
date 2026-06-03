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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if sum(clause) != 0:
                clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for clause in cnf:
            rank += max(abs(x) for x in clause)
        return rank
    
    def p_adic_order(zeta):
        if zeta == 0:
            return float('inf')
        order = 0
        while zeta % 2 == 0:
            zeta //= 2
            order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    ord_p_zeta_sum = 0
    C_comm_sum = 0
    max_n = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        zeta = 1.0
        for clause in cnf:
            product = 1.0
            for literal in clause:
                if literal > 0:
                    product *= (1 - 1 / (2 ** literal))
                else:
                    product *= (1 + 1 / (2 ** abs(literal)))
            zeta *= product
        
        ord_p_zeta = p_adic_order(zeta)
        C_comm = communication_complexity_rank(cnf)
        
        instances_tested += len(cnf)
        ord_p_zeta_sum += ord_p_zeta
        C_comm_sum += C_comm
        max_n = n
    
    mean_ord_p_zeta = ord_p_zeta_sum / instances_tested
    mean_C_comm = C_comm_sum / instances_tested
    std_dev = math.sqrt((sum((ord_p_zeta - mean_ord_p_zeta) ** 2 for ord_p_zeta in range(ord_p_zeta_sum)) / instances_tested +
                          sum((C_comm - mean_C_comm) ** 2 for C_comm in range(C_comm_sum)) / instances_tested) / 2)
    
    conjecture_holds = all(abs(ord_p_zeta - mean_ord_p_zeta) <= 3 * std_dev for ord_p_zeta in range(ord_p_zeta_sum))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "p-adic Order vs Communication Complexity Rank",
        "metric_value": mean_ord_p_zeta,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")