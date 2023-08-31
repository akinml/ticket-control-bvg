from sklearn.pipeline import Pipeline, make_pipeline

pipeline = Pipeline([
    ('cleaner', data_cleaning())),
    ('fuzzer', fuzz_flow())
])
