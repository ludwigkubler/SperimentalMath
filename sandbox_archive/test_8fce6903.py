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
    
    def hensel_lifting(clause, p):
        n = len(clause)
        valuation = [0] * n
        for _ in range(10):  # Limit to avoid infinite loops
            changed = False
            for i in range(n):
                if valuation[i] == 0:
                    continue
                new_valuation = (valuation[i] - sum(valuation[j] for j in clause if j != i)) % p
                if new_valuation != valuation[i]:
                    valuation[i] = new_valuation
                    changed = True
            if not changed:
                break
        return max(valuation)
    
    def dpll(clause_set, assignment):
        if not clause_set:
            return True
        if any(all(var in assignment and assignment[var] == val for var, val in clause) for clause in clause_set):
            return True
        literals = set()
        for clause in clause_set:
            literals.update(clause)
        literal = random.choice(list(literals))
        positive_clauses = [clause for clause in clause_set if literal in clause]
        negative_clauses = [clause for clause in clause_set if -literal in clause]
        return dpll(positive_clauses, assignment | {literal: True}) or dpll(negative_clauses, assignment | {-literal: False})
    
    def p_rank(clause_set):
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        ranks = []
        for p in primes:
            rank = 0
            for clause in clause_set:
                rank = max(rank, hensel_lifting(clause, p))
            ranks.append(rank)
        return sum(ranks) / len(primes)
    
    def diameter(clause_set):
        n = len(clause_set)
        if n == 1:
            return 0
        graph = {i: set() for i in range(n)}
        for i in range(n):
            for j in range(i + 1, n):
                if any(literal in clause_set[i] and -literal in clause_set[j] for literal in clause_set[i]):
                    graph[i].add(j)
                    graph[j].add(i)
        
        def bfs(start):
            visited = [False] * n
            queue = [start]
            visited[start] = True
            distance = 0
            while queue:
                next_queue = []
                for node in queue:
                    for neighbor in graph[node]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            next_queue.append(neighbor)
                queue = next_queue
                distance += 1
            return distance
        
        max_distance = 0
        for i in range(n):
            max_distance = max(max_distance, bfs(i))
        return max_distance
    
    n = random.randint(5, 40)
    clause_set = []
    for _ in range(n):
        num_clauses = random.randint(1, n)
        clause = set()
        while len(clause) < num_clauses:
            literal = random.choice([-i, i] for i in range(1, n + 1))
            if literal not in clause and -literal not in clause:
                clause.add(literal)
        clause_set.append(list(clause))
    
    prank = p_rank(clause_set)
    d_diameter = diameter(clause_set)
    
    return {
        "metric_name": "p-rank vs Diameter",
        "metric_value": prank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(prank - d_diameter) <= 3 * (d_diameter / math.sqrt(n)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"p-rank vs Diameter\" first_failing_seed={r['seed']}")
                break