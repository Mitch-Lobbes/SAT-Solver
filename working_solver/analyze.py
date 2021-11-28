import pandas

DPLL = "results/Algorithm.DPLL.csv"
JEROSLOW = "results/Algorithm.JEROSLOW_WANG.csv"
DYNAMIC = "results/Algorithm.DYNAMIC_VARIABLE_ORDERING.csv"


df = pandas.read_csv(DPLL)
print(df)