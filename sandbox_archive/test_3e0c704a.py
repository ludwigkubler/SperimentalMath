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
        gate_type = random.choice(['AND', 'OR', 'NOT', 'XOR'])
        num_inputs = random.randint(1, min(3, n))
        inputs = random.sample(range(len(gates)), num_inputs) if gates else []
        gates.append((gate_type, inputs))
    return gates

def compute_truth_table(circuit, n):
    tt = {}
    for inputs in itertools.product([0, 1], repeat=n):
        tt[inputs] = evaluate_circuit(circuit, inputs)
    return tt

def evaluate_circuit(circuit, inputs):
    values = list(inputs)
    for gate_type, gate_inputs in circuit:
        if gate_type == 'AND':
            val = 1
            for i in gate_inputs:
                val &= values[i]
            values.append(val)
        elif gate_type == 'OR':
            val = 0
            for i in gate_inputs:
                val |= values[i]
            values.append(val)
        elif gate_type == 'NOT':
            val = 1 - values[gate_inputs[0]]
            values.append(val)
        elif gate_type == 'XOR':
            val = values[gate_inputs[0]] ^ values[gate_inputs[1]]
            values.append(val)
    return values[-1]

def compute_supports(circuit, n):
    supports = []
    for gate_type, gate_inputs in circuit:
        if gate_type == 'AND':
            supp = set()
            for i in gate_inputs:
                supp.update(supports[i])
            supports.append(supp)
        elif gate_type == 'OR':
            supp = set()
            for i in gate_inputs:
                supp.update(supports[i])
            supports.append(supp)
        elif gate_type == 'NOT':
            supp = supports[gate_inputs[0]].copy()
            supports.append(supp)
        elif gate_type == 'XOR':
            supp = supports[gate_inputs[0]].copy()
            supp.update(supports[gate_inputs[1]])
            supports.append(supp)
    return supports

def build_gate_conflict_graph(supports):
    graph = defaultdict(set)
    for i in range(len(supports)):
        for j in range(i + 1, len(supports)):
            if supports[i] & supports[j]:
                graph[i].add(j)
                graph[j].add(i)
    return graph

def count_independent_sets(graph):
    nodes = list(graph.keys())
    count = 0
    for r in range(len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            is_independent = True
            for i in range(len(subset)):
                for j in range(i + 1, len(subset)):
                    if subset[j] in graph[subset[i]]:
                        is_independent = False
                        break
                if not is_independent:
                    break
            if is_independent:
                count += (-1) ** len(subset)
    return count

def compute_tau(graph):
    return abs(count_independent_sets(graph))

def compute_agreement(tt, mod_q):
    n = len(next(iter(tt.keys())))
    count = 0
    for inputs in tt:
        if tt[inputs] == (sum(inputs) % mod_q):
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
                    supports = compute_supports(circuit, n)
                    graph = build_gate_conflict_graph(supports)
                    tau = compute_tau(graph)
                    agreement = compute_agreement(tt, mod_q)

                    if agreement >= (1 - epsilon) * (2 ** n):
                        predicted_bound = 2 ** (n / (10 * d ** 2)) - 1
                        if tau < predicted_bound:
                            conjecture_holds = False
                            counterexample = f"n={n}, d={d}, s={s}, mod_q={mod_q}, tau={tau}, predicted_bound={predicted_bound}"
                            return {
                                "metric_name": "tau",
                                "metric_value": tau,
                                "instances_tested": instances_tested + 1,
                                "conjecture_holds": conjecture_holds,
                                "counterexample": counterexample
                            }
                        metric_values.append(tau)
                        instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "tau",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": True,
            "counterexample": ""
        }

    return {
        "metric_name": "tau",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]

    metric_values = []
    instances_tested = 0
    conjecture_holds_count = 0
    first_failing_seed = None

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        instances_tested += result["instances_tested"]
        if result["conjecture_holds"]:
            conjecture_holds_count += 1
        else:
            if first_failing_seed is None:
                first_failing_seed = seed

    if instances_tested == 0:
        print("RESULT: INCONCLUSIVE reason=no_instances_tested")
        sys.exit(0)

    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = conjecture_holds_count / len(seeds)

    if first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")