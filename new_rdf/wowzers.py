fl = open("data_test_fix.n3", "r")

genres_set = set()
genres_used_set = set()


for line in fl:
    # spot:g1 dc:title "432hz"^^w3:string ;
    if line.startswith("spot:g"):
        line1 = line.split(";")[0].split(" dc:title")[0].split(":")[1].strip()
        genres_set.add(line1)
    if line.startswith("spot:a"):
        line2 = line.split(";")[-1].split(":")[-1][:-3].strip()
        genres_used_set.add(line2)

print(len(genres_set), len(genres_used_set))

unused_genres_set = genres_set - genres_used_set




real_data_file = open("data_test5_2.n3", "r")

second_data_file = open("data_test5_fix.n3", "w")

for line in real_data_file:
    if line.startswith("spot:g"):
        genre_id = line.split(";")[0].split(" dc:title")[0].split(":")[1].strip()
        if not genre_id in unused_genres_set:
            second_data_file.write(line)
    else:
        second_data_file.write(line)
