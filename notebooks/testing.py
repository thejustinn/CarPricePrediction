from test_pipe import DataPipeLine

pipeline = DataPipeLine('CarPricePrediction/notebooks/sgcarmart_used_cars_prices7.csv')


print(pipeline.run_pipeline())

