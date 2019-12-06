from os import walk

f = []
for (dirpath, dirnames, filenames) in walk("./"):
    f.extend(filenames)


best_training = 0
best_training_file = ''
best_test = 0
best_test_file = ''

for file in filenames:
    if(file[-3:] == ".py"):
        continue
    lines = open(file, "r").readlines()
    for line in lines:
        line_split = line.split("=")
        if line_split[0] == "training_score":
            training_value = float(line_split[1].replace('\n', ''))
            if training_value > best_training:
                best_training = training_value
                best_training_file = file
        elif line_split[0] == "test_score":
            test_score = float(line_split[1].replace('\n', ''))
            if test_score > best_test:
                best_test = test_score
                best_test_file = file


print("Best training: " + str(best_training) + " - File: " + best_training_file)
print("Best test: " + str(best_test) + " - File: " + best_test_file)
