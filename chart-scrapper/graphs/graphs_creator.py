import os
import json
import numpy as np
import matplotlib.pyplot as plt

files = os.listdir("../logs")


training_scores = []
test_scores = []
str_labels = []

for file in files:
    with open(f'../logs/{file}') as json_file:
        json_file = json.load(json_file)
        number_of_labels = json_file['number_of_labels']
        training_score = json_file['training_score']
        test_score = json_file['test_score']
        layers = json_file['layers']

        final_label = str(layers) + " - " + str(number_of_labels)

        training_score.append(training_score)
        test_score.append(test_score)
        str_labels.append(final_label)

# # data to plot
n_groups = len(files)

# # create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
opacity = 0.8


rect1 = plt.bar(index, training_scores, bar_width, alpha=opacity, color='b', label='Training Scores')
rect2 = plt.bar(index, test_scores, bar_width, alpha=opacity, color='b', label='Test Scores')

plt.xlabel('Configuration')
plt.ylabel('Scores')
plt.title('Scores by configuration and number of labels')
plt.xticks(index + bar_width, str_labels)
plt.legend()

plt.tight_layout()
plt.show()
