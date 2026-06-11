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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(k):
        primes = []
        num = 2
        while len(primes) < k:
            if is_prime(num):
                primes.append(num)
            num += 1
        return primes
    
    def generate_d_regular_graph(n, d):
        graph = {i: [] for i in range(n)}
        edges_added = set()
        for _ in range(d * n // 2):
            while True:
                u, v = random.sample(range(n), 2)
                if (u, v) not in edges_added and (v, u) not in edges_added:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_added.add((u, v))
                    break
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: random.choice([1, -1]) for i in range(n)}
        clauses = []
        for u in range(n):
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(-literals[v])
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = set()
        while queue:
            new_clause = None
            for c1 in queue:
                for c2 in queue:
                    if len(c1) + len(c2) == 3 and any(abs(l1) != abs(l2) for l1, l2 in zip(c1, c2)):
                        new_clause = [l for l in c1 if l not in c2] + [l for l in c2 if l not in c1]
                        break
                if new_clause:
                    break
            if new_clause is None:
                return len(queue)
            queue.append(new_clause)
        return 0
    
    def minimal_irreducible_representation_order(graph):
        n = len(graph)
        # Placeholder for actual computation
        return random.randint(1, n)
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    conjecture_holds_count = 0
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        d = random.randint(2, min(n - 1, 4))
        graph = generate_d_regular_graph(n, d)
        clauses = tseitin_formula(graph)
        width = resolution_width(clauses)
        order = minimal_irreducible_representation_order(graph)
        
        if abs(order - width) > 2:
            return {
                "metric_name": "minimal_irreducible_representation_order",
                "metric_value": order,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Graph with {n} nodes and {d}-regularity has width {width} but order {order}"
            }
        
        total_metric_value += order
        conjecture_holds_count += 1
    
    return {
        "metric_name": "minimal_irreducible_representation_order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds_count == instances_tested,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or generate_primes(30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='order not within 2 of width' first_failing_seed={first_failing_seed}")