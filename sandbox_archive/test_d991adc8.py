# auto-injected by SEC sandbox
import json
import os
import time
import re
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from collections import defaultdict

def generate_random_circuit(n, d, s):
    gates = []
    for _ in range(s):
        if random.random() < 0.5:
            gates.append(('AND', []))
        else:
            gates.append(('OR', []))
    for i in range(len(gates)):
        if gates[i][0] in ['AND', 'OR']:
            num_inputs = random.randint(2, min(3, n))
            inputs = random.sample(range(n), num_inputs) if n > 0 else []
            gates[i] = (gates[i][0], inputs)
    return gates

def compute_truth_table(circuit, n):
    if n > 10:
        return None
    tt = {}
    for inputs in itertools.product([0, 1], repeat=n):
        output = 1
        for gate in circuit:
            if gate[0] == 'AND':
                gate_output = 1
                for i in gate[1]:
                    if i < len(inputs):
                        gate_output &= inputs[i]
                output &= gate_output
            elif gate[0] == 'OR':
                gate_output = 0
                for i in gate[1]:
                    if i < len(inputs):
                        gate_output |= inputs[i]
                output |= gate_output
        tt[inputs] = output
    return tt

def compute_supp(gate, n):
    if gate[0] == 'AND':
        return set(gate[1])
    elif gate[0] == 'OR':
        return set(gate[1])
    return set()

def build_gate_conflict_graph(circuit, n):
    graph = defaultdict(set)
    gates = [g for g in circuit if g[0] in ['AND', 'OR']]
    for i, g1 in enumerate(gates):
        for j, g2 in enumerate(gates):
            if i != j:
                supp1 = compute_supp(g1, n)
                supp2 = compute_supp(g2, n)
                if supp1 & supp2:
                    graph[i].add(j)
    return graph

def is_independent_set(graph, S):
    for i in S:
        for j in S:
            if i != j and j in graph[i]:
                return False
    return True

def compute_tau(graph):
    independent_sets = []
    for k in range(1, len(graph) + 1):
        for S in itertools.combinations(graph.keys(), k):
            if is_independent_set(graph, S):
                independent_sets.append(S)
    tau = 0
    for S in independent_sets:
        tau += (-1) ** len(S)
    return abs(tau)

def compute_agreement(tt, mod_q, n):
    if tt is None:
        return 0
    count = 0
    for inputs in tt:
        x = sum(inputs) % mod_q
        if tt[inputs] == (x == 0):
            count += 1
    return count / (2 ** n)

def run_trial(seed):
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    d_values = [2, 3, 4]
    s_values = [8, 12, 16, 20]
    mod_q_values = [3, 5]
    epsilon = 1/4

    metric_values = []
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for d in d_values:
            for s in s_values:
                for mod_q in mod_q_values:
                    circuit = generate_random_circuit(n, d, s)
                    tt = compute_truth_table(circuit, n)
                    if tt is None:
                        continue
                    graph = build_gate_conflict_graph(circuit, n)
                    tau = compute_tau(graph)
                    agreement = compute_agreement(tt, mod_q, n)
                    threshold = (1 - epsilon) * (2 ** n)
                    predicted_bound = 2 ** (n / (10 * d ** 2)) - 1

                    if agreement >= threshold and tau < predicted_bound:
                        conjecture_holds = False
                        counterexample = f"n={n}, d={d}, s={s}, mod_q={mod_q}, tau={tau}, predicted_bound={predicted_bound}"
                        break

                    metric_values.append(tau)
                    instances_tested += 1

                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if not metric_values:
        return {
            "metric_name": "tau",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "tau",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["metric_value"] != 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample={results[0]['counterexample']} first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")