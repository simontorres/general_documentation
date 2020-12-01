awk '{print "sed -i \"s/date = '\''2019-08-06'\''/date = '\''"$1"'\''/g\" 2019B_flats_"$1".ipynb"}' nights-list.txt
