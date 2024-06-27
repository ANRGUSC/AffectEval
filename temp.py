import matplotlib.pyplot as plt
import numpy as np


# ACC/AUC for ensemble of models
apd = [0.645, 0.608]
wesad = [0.99, 0.969]
case = [0.813, 0.736]

# Cross-corpus
apd_case = [0.708, 0.611]
case_apd = [0.567, 0.551]
apd_wesad = [0.658, 0.709]
wesad_apd = [0.569, 0.561]
wesad_case = [0.644, 0.6]
case_wesad = [0.759, 0.591]

# acc = {
#     "Test on WESAD": [wesad[0], apd_wesad[0], case_wesad[0]],
#     "Test on APD": [apd[0], wesad_apd[0], case_apd[0]],
#     "Test on CASE": [case[0], apd_case[0], wesad_case[0]]
# }

acc = {
    "Same dataset": [wesad[0], apd[0], case[0]],
    "Same label": [apd_wesad[0], wesad_apd[0]],
    "Across labels": [case_wesad[0], case_apd[0], wesad_case[0], apd_case[0]]
}

acc1 = acc["Same dataset"]
acc2 = acc["Same label"]
acc3 = acc["Across labels"]

# auc = {
#     "Test on WESAD": [wesad[1], apd_wesad[1], case_wesad[1]],
#     "Test on APD": [apd[1], wesad_apd[1], case_apd[1]],
#     "Test on CASE": [case[1], apd_case[1], wesad_case[1]]
# }

auc = {
    "Same dataset": [wesad[1], apd[1], case[1]],
    "Same label": [apd_wesad[1], wesad_apd[1]],
    "Across labels": [case_wesad[1], case_apd[1], wesad_case[1], apd_case[1]]
}

groups = list(acc.keys())

# x = np.arange(len(groups))  # label locations
# width = 0.25  # width of the bars
# multiplier = 0

width = 1
groupgap = 1
x1 = np.arange(len(acc1))
x2 = np.arange(len(acc2))+groupgap+len(acc1)
x3 = np.arange(len(acc3))+groupgap+len(acc2)+groupgap+len(acc1)
ind = np.concatenate((x1, x2, x3))

fig, ax = plt.subplots(figsize=(8, 3))

# for title, measurement in acc.items():
#     offset = width * multiplier
#     rects = ax.bar(x + offset, measurement, width, label=title)
#     ax.bar_label(rects, padding=3)
#     multiplier += 1

rects1 = ax.bar(x1, acc1, width, color='darkseagreen', edgecolor='black', label=groups[0])
rects2 = ax.bar(x2, acc2, width, color='cadetblue', edgecolor='black', label=groups[1])
rects2 = ax.bar(x3, acc3, width, color='mediumpurple', edgecolor='black', label=groups[2])

ax.set_title("Testing accuracy", fontsize=14)
ax.set_ylabel("Acc", fontsize=14)
ax.set_xticks(ind)
ax.set_xticklabels(('WESAD', 'APD', 'CASE', 'APD/WESAD', 'WESAD/APD', 'CASE/WESAD', 'CASE/APD', 'WESAD/CASE', 'APD/CASE'), rotation=30, ha='right', fontsize=12)
plt.legend(loc="lower right")

plt.show()