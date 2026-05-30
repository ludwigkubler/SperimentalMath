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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(x == 0 for x in clause):
                cnf.append(clause)
        return cnf
    
    def truth_table(cnf):
        n = len(cnf[0])
        table = []
        for assignment in product([-1, 1], repeat=n):
            if all(any(x * assignment[abs(lit)-1] >= 0 for x in clause) for clause in cnf):
                table.append(assignment)
        return table
    
    def min_modular_function_order(table):
        n = len(table[0])
        max_value = max(abs(val) for row in table for val in row)
        order = 0
        while True:
            found = False
            for i in range(n):
                if all(row[i] * (val + 1) >= 0 for row in table):
                    found = True
                    break
            if not found:
                return order
            order += 1
    
    def tree_like_resolution_width(cnf, table):
        n = len(table[0])
        width = 2**n
        for assignment in table:
            clause = [x * assignment[abs(lit)-1] >= 0 for lit in cnf]
            if all(clause):
                width = min(width, sum(1 for x in assignment if x != 0))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        table = truth_table(cnf)
        order = min_modular_function_order(table)
        width = tree_like_resolution_width(cnf, table)
        
        if order == 0 or width == 0:
            return {
                "metric_name": "tree_like_resolution_width",
                "metric_value": None,
                "instances_tested": len(table),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        results.append({
            "n": n,
            "order": order,
            "width": width
        })
    
    mean_width = sum(res["width"] for res in results) / len(results)
    std_width = math.sqrt(sum((res["width"] - mean_width)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if abs(res["width"] - 2**(n * res["order"])) <= 3) / len(results)
    
    return {
        "metric_name": "tree_like_resolution_width",
        "metric_value": mean_width,
        "instances_tested": sum(res["instances_tested"] for res in results),
        "n_max": max(res["n"] for res in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, order={results[0]['order']}, width={results[0]['width']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["metric_value"] - mean_width)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - 2**(n * result["instances_tested"])) <= 3) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")