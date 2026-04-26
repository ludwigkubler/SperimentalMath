import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    rank = 0
    for j in range(n):
        i_max = rank
        for i in range(rank, m):
            if abs(A[i][j]) > abs(A[i_max][j]):
                i_max = i
        A[rank], A[i_max] = A[i_max], A[rank]
        if A[rank][j] != 0:
            for i in range(m):
                if i != rank and A[i][j] != 0:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
    return rank

def count_solutions(A):
    rank = gaussian_elimination(A)
    free_vars = len(A[0]) - rank
    if rank < len(A):
        return 2 ** free_vars
    else:
        return 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 8, 11, 14]
    total_solutions = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        m = random.randint(2 * n, 3 * n)
        solutions = []
        for _ in range(m):
            A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
            A += [[random.choice([-1, 1]) for _ in range(n + 1)]]
            solutions.append(count_solutions(A))
        
        total_solutions += sum(solutions)
        instances_tested += len(solutions)

    average_solution_count = total_solutions / instances_tested
    log_n = math.log(n_values[-1])
    exponent_estimate = (average_solution_count / (2 ** n_values[-1])) / log_n

    if exponent_estimate < 0.5 or exponent_estimate > 1.5:
        conjecture_holds = False
        counterexample = "Exponent out of expected range"

    return {
        "metric_name": "Average Solution Count Exponent",
        "metric_value": exponent_estimate,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_exponent = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_exponent) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_exponent} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Exponent out of expected range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")