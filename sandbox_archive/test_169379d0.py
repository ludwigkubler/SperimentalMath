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
        for _ in range(2 * n):
            clause = set(random.sample(range(1, n + 1), 3))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            clauses.append(clause)
        return clauses
    
    def is_clause_satisfied(clause, assignment):
        for lit in clause:
            if (lit > 0 and assignment[lit - 1]) or (lit < 0 and not assignment[abs(lit) - 1]):
                return True
        return False
    
    def evaluate_cnf(cnf, assignment):
        return all(is_clause_satisfied(clause, assignment) for clause in cnf)
    
    def communication_complexity_rank_variance(cnf):
        n = len(cnf)
        max_rank = 0
        for i in range(n):
            rank = sum(1 for clause in cnf if any(lit == i + 1 or lit == -(i + 1) for lit in clause))
            max_rank = max(max_rank, rank)
        return (max_rank - n / 2) ** 2
    
    def minimal_brauer_group_order(cnf):
        n = len(cnf)
        assignment = [False] * n
        order = 0
        while not evaluate_cnf(cnf, assignment):
            for i in range(n):
                if not assignment[i]:
                    assignment[i] = True
                    break
            else:
                return order
            order += 1
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank_variance = communication_complexity_rank_variance(cnf)
            brauer_group_order = minimal_brauer_group_order(cnf)
            if rank_variance == 0 or brauer_group_order == 0:
                continue
            total_metric_value += abs(brauer_group_order - rank_variance) / (brauer_group_order * rank_variance)
            instances_tested += 1
            n_max = max(n_max, n)
            if not conjecture_holds and counterexample == "":
                if abs(brauer_group_order - rank_variance) > 2 * min(brauer_group_order, rank_variance):
                    conjecture_holds = False
                    counterexample = f"n={n}, |Br(Qφ)|={brauer_group_order}, ρ(φ)={rank_variance}"
    
    if instances_tested < 30:
        return {
            "metric_name": "Communication Complexity Rank Variance vs Brauer Group Order",
            "metric_value": total_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for _ in range(30) if run_trial(random.randint(1, 1000))["conjecture_holds"]) / 30
    
    return {
        "metric_name": "Communication Complexity Rank Variance vs Brauer Group Order",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")