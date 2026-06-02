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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def permutation_action(cnf, var):
        action = {}
        for clause in cnf:
            if var in clause:
                new_clause = [v if v != var else -var for v in clause]
                action[tuple(sorted(new_clause))] = True
        return action
    
    def linear_representation(action):
        rep = {}
        for key, _ in action.items():
            if key not in rep:
                rep[key] = len(rep) + 1
        return rep
    
    def communication_complexity_rank(cnf):
        rank = 0
        seen = set()
        for clause in cnf:
            clause_set = frozenset(clause)
            if clause_set not in seen:
                seen.add(clause_set)
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order_sum = 0
        rank_sum = 0
        instances = 0
        
        while instances < 30:
            action = permutation_action(cnf, random.randint(1, n))
            rep = linear_representation(action)
            min_order = max(rep.values())
            rank = communication_complexity_rank(cnf)
            
            if min_order <= 0 or rank <= 0:
                continue
            
            min_order_sum += min_order
            rank_sum += rank
            instances += 1
            instances_tested += 1
            n_max = max(n_max, n)
        
        if instances > 0:
            avg_min_order = min_order_sum / instances
            avg_rank = rank_sum / instances
            correlation_coefficient = (instances * avg_min_order * avg_rank - sum(min_order * rank for min_order, rank in zip(rep.values(), rep.values()))) / math.sqrt((instances * sum(min_order ** 2 for min_order in rep.values()) - sum(min_order ** 2 for min_order in rep.values())) * (instances * sum(rank ** 2 for rank in rep.values()) - sum(rank ** 2 for rank in rep.values())))
            
            if correlation_coefficient < 0.7:
                conjecture_holds = False
                counterexample = f"n={n}, avg_min_order={avg_min_order}, avg_rank={avg_rank}, correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": total_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded n_tested={len(results)}")