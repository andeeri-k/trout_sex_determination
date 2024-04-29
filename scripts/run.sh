python3 simulated_data.py
python3 model_xgboost.py sim_5.dat sim_5.bin > sim_5.log
python3 model_xgboost.py sim_50.dat sim_50_model.bin > sim_50.log
python3 model_xgboost.py sim_real.dat sim_real.bin > sim_real.log
python3 model_xgboost.py sim_random.dat sim_random.bin > sim_random.log
