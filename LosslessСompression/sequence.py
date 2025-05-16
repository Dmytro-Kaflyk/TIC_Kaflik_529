import os
import random
import collections
import math
import string
import matplotlib.pyplot as plt

N_sequence = 100
your_surname = "кафлик"
your_student_number = 8
your_group_number = "529"

list1 = ['1'] * your_student_number
list0 = ['0'] * (N_sequence - your_student_number)
original_sequence_1 = list1 + list0
random.shuffle(original_sequence_1)
original_sequence_1 = ''.join(original_sequence_1)

list2 = list(your_surname) + ['0'] * (N_sequence - len(your_surname))
original_sequence_2 = ''.join(list2)

list3 = list(your_surname) + ['0'] * (N_sequence - len(your_surname))
random.shuffle(list3)
original_sequence_3 = ''.join(list3)

letters = list(your_surname) + list(your_group_number)
n_letters = len(letters)
n_repeats = N_sequence // n_letters
remainder = N_sequence % n_letters
list4 = letters * n_repeats + letters[:remainder]
original_sequence_4 = ''.join(list4)

elements_5 = list(your_surname[:2]) + list(your_group_number)
original_sequence_5 = random.choices(elements_5, k=N_sequence)
random.shuffle(original_sequence_5)
original_sequence_5 = ''.join(original_sequence_5)

letters_6 = list(your_surname[:2])
digits_6 = list(your_group_number)
n_letters_6 = int(0.7 * N_sequence)
n_digits_6 = N_sequence - n_letters_6
list6 = random.choices(letters_6, k=n_letters_6) + random.choices(digits_6, k=n_digits_6)
random.shuffle(list6)
original_sequence_6 = ''.join(list6)

elements_7 = list(string.ascii_lowercase) + list(string.digits)
original_sequence_7 = ''.join(random.choices(elements_7, k=N_sequence))

original_sequence_8 = '1' * N_sequence

original_sequences = [
    original_sequence_1,
    original_sequence_2,
    original_sequence_3,
    original_sequence_4,
    original_sequence_5,
    original_sequence_6,
    original_sequence_7,
    original_sequence_8
]

os.makedirs("LosslessСompression", exist_ok=True)

with open("LosslessСompression/sequence.txt", "w", encoding="utf-8") as seq_file:
    for seq in original_sequences:
        seq_file.write(seq + "\n")

results = []
with open("LosslessСompression/results_sequence.txt", "w", encoding="utf-8") as results_file:
    for i, sequence in enumerate(original_sequences, 1):
        counts = collections.Counter(sequence)
        sequence_alphabet_size = len(counts)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        mean_probability = sum(probability.values()) / sequence_alphabet_size
        equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
        uniformity = "рівна" if equal else "нерівна"
        entropy = -sum(p * math.log2(p) for p in probability.values())
        if sequence_alphabet_size > 1:
            source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
        else:
            source_excess = 1
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])

        results_file.write(f"Sequence {i}:\n")
        results_file.write(f"Ймовірності: {probability_str}\n")
        results_file.write(f"Середня ймовірність: {mean_probability:.4f}\n")
        results_file.write(f"Тип розподілу: {uniformity}\n")
        results_file.write(f"Ентропія: {entropy:.4f}\n")
        results_file.write(f"Надмірність джерела: {source_excess:.4f}\n\n")

        results.append([sequence_alphabet_size, round(entropy, 2), round(source_excess, 2), uniformity])

fig, ax = plt.subplots(figsize=(14 / 1.54, len(original_sequences) / 1.54))
headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
rows = [f"Послідовність {i}" for i in range(1, len(original_sequences) + 1)]
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig("LosslessСompression/Характеристики сформованих послідовностей.png")
plt.show()
