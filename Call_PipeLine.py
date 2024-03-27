from DataPipeLine import DataPipeLine

pipeline = DataPipeLine('CarPricePrediction/sgcarmart_used_cars_prices7.csv')


print(pipeline.run_pipeline())

