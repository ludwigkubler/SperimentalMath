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
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            for other_clause in queue + seen:
                if any(abs(x) == abs(y) and (x != y) for x, y in zip(clause, other_clause)):
                    new_clause = [x for x in clause if x not in other_clause]
                    new_clause.extend([y for y in other_clause if -y not in clause])
                    if len(new_clause) == 0:
                        return float('inf')
                    new_clause = list(set(new_clause))
                    if tuple(sorted(new_clause)) not in seen:
                        queue.append(new_clause)
                        seen.add(tuple(sorted(new_clause)))
        return len(queue)
    
    def formal_context(cnf):
        universe = set(range(1, len(cnf) + 1))
        minterms = [tuple([x for x in clause if x > 0]) for clause in cnf]
        non_minterms = [tuple([-x for x in clause if x < 0]) for clause in cnf]
        universe.update(minterms)
        universe.update(non_minterms)
        relation = {(x, y): (x in minterms and y in minterms) or (x in non_minterms and y in non_minterms) for x in universe for y in universe}
        return relation
    
    def min_rank(relation):
        n = len(relation)
        matrix = [[0] * n for _ in range(n)]
        for i, j in relation:
            if relation[(i, j)]:
                matrix[i-1][j-1] = 1
                matrix[j-1][i-1] = 1
        rank = 0
        for row in matrix:
            if any(x != 0 for x in row):
                rank += 1
                for i in range(n):
                    if matrix[i][row.index(1)] == 1:
                        for j in range(n):
                            matrix[i][j] ^= matrix[row.index(1)][j]
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        context = formal_context(cnf)
        rank = min_rank(context)
        results.append({
            "n": n,
            "width": width,
            "rank": rank
        })
    
    if not all(result["width"] != float('inf') for result in results):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "resolution_width_infinite"
        }
    
    widths = [result["width"] for result in results]
    ranks = [result["rank"] for result in results]
    
    mean_rank = sum(ranks) / len(ranks)
    std_rank = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    correlation_coefficient = sum((widths[i] - mean(widths)) * (ranks[i] - mean_ranks) for i in range(len(results))) / (len(results) * std_widths * std_ranks)
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and all(abs(ranks[i] - math.log(widths[i])) <= 5 for i in range(len(results))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) > 5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_exceeds_log_width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")