fl = open("data_test5_fix.n3", "r")

fo = open("data_fix_part0.n3", "w")
fl_count = 1
output = False
for count, line in enumerate(fl):
    fo.write(line)
    if count!=0 and (count%1000000)==0:
        output = True
    if output and line == "\n":
        fo = open(f"data_fix_part{fl_count}.n3", "w")
        fl_count += 1
        output = False


