awk '{print "jupyter nbconvert --ExecutePreprocessor.timeout=-1  --execute --to notebook --inplace 2019B_bias_"$1".ipynb"}' nights-list.txt
