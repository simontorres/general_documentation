awk '{if (NR > 8) print "jupyter nbconvert --ExecutePreprocessor.timeout=-1  --execute --to notebook --inplace 2019B_flats_"$1".ipynb"}' nights-list.txt
