# -*- coding: utf-8 -*-

import math
from collections import Counter

ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

# 🔐 ФИКСИРОВАННЫЙ АЛФАВИТ ЗАМЕНЫ (ПОСТОЯННЫЙ)
SUBSTITUTION_ALPHABET = "ЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБА"

M = len(ALPHABET)


# ==========================================
# ВСПОМОГАТЕЛЬНЫЕ
# ==========================================

def mod_inverse(a, m):
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None


def clean_text(text):
    return text.upper()


# ==========================================
# 1. ПРОСТАЯ ЗАМЕНА (ФИКСИРОВАННАЯ)
# ==========================================

def simple_sub_encrypt(text):
    return "".join(
        SUBSTITUTION_ALPHABET[ALPHABET.index(c)] if c in ALPHABET else c
        for c in text
    )


def simple_sub_decrypt(text):
    return "".join(
        ALPHABET[SUBSTITUTION_ALPHABET.index(c)] if c in SUBSTITUTION_ALPHABET else c
        for c in text
    )


# ==========================================
# 2. АФФИННЫЙ
# ==========================================

def affine_encrypt(text, a, b):
    if math.gcd(a, M) != 1:
        print("❌ a должно быть взаимно просто с 33!")
        return None

    return "".join(
        ALPHABET[(a * ALPHABET.index(c) + b) % M] if c in ALPHABET else c
        for c in text
    )


def affine_decrypt(text, a, b):
    a_inv = mod_inverse(a, M)

    if a_inv is None:
        print("❌ Нет обратного элемента!")
        return None

    return "".join(
        ALPHABET[(a_inv * (ALPHABET.index(c) - b)) % M] if c in ALPHABET else c
        for c in text
    )


# ==========================================
# 3. АФФИННЫЙ РЕКУРРЕНТНЫЙ
# ==========================================

def affine_recursive_encrypt(text, a1, b1, a2, b2):
    result = ""
    a_prev2, b_prev2 = a1, b1
    a_prev1, b_prev1 = a2, b2

    for i, char in enumerate(text):
        if char not in ALPHABET:
            result += char
            continue

        x = ALPHABET.index(char)

        if i == 0:
            a, b = a1, b1
        elif i == 1:
            a, b = a2, b2
        else:
            a = (a_prev1 * a_prev2) % M
            b = (b_prev1 + b_prev2) % M
            a_prev2, b_prev2 = a_prev1, b_prev1
            a_prev1, b_prev1 = a, b

        y = (a * x + b) % M
        result += ALPHABET[y]

    return result


def affine_recursive_decrypt(text, a1, b1, a2, b2):
    result = ""
    a_prev2, b_prev2 = a1, b1
    a_prev1, b_prev1 = a2, b2

    for i, char in enumerate(text):
        if char not in ALPHABET:
            result += char
            continue

        y = ALPHABET.index(char)

        if i == 0:
            a, b = a1, b1
        elif i == 1:
            a, b = a2, b2
        else:
            a = (a_prev1 * a_prev2) % M
            b = (b_prev1 + b_prev2) % M
            a_prev2, b_prev2 = a_prev1, b_prev1
            a_prev1, b_prev1 = a, b

        a_inv = mod_inverse(a, M)
        if a_inv is None:
            print("❌ Невозможно расшифровать!")
            return None

        x = (a_inv * (y - b)) % M
        result += ALPHABET[x]

    return result


# ==========================================
# МЕНЮ
# ==========================================

def main():
    print("=" * 60)
    print("МОНОАЛФАВИТНЫЕ ПОДСТАНОВОЧНЫЕ ШИФРЫ")
    print("=" * 60)

    text = clean_text(input("Введите текст: "))

    print("\n1 - Простая замена (фиксированный алфавит)")
    print("2 - Аффинный")
    print("3 - Аффинный рекуррентный")

    choice = input("Ваш выбор: ")

    if choice == "1":
        mode = input("E - шифрование, D - дешифрование: ").upper()

        if mode == "E":
            result = simple_sub_encrypt(text)
        elif mode == "D":
            result = simple_sub_decrypt(text)
        else:
            print("❌ Неверный режим!")
            return

    elif choice == "2":
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        mode = input("E - шифрование, D - дешифрование: ").upper()

        if mode == "E":
            result = affine_encrypt(text, a, b)
        elif mode == "D":
            result = affine_decrypt(text, a, b)
        else:
            print("❌ Неверный режим!")
            return

    elif choice == "3":
        a1 = int(input("Введите a1: "))
        b1 = int(input("Введите b1: "))
        a2 = int(input("Введите a2: "))
        b2 = int(input("Введите b2: "))
        mode = input("E - шифрование, D - дешифрование: ").upper()

        if mode == "E":
            result = affine_recursive_encrypt(text, a1, b1, a2, b2)
        elif mode == "D":
            result = affine_recursive_decrypt(text, a1, b1, a2, b2)
        else:
            print("❌ Неверный режим!")
            return

    else:
        print("❌ Неверный выбор!")
        return

    print("\n🔎 РЕЗУЛЬТАТ:")
    print(result)

    freq = Counter([c for c in result if c in ALPHABET])
    print("\n📊 Частотный анализ:")
    for char, count in freq.most_common():
        print(char, ":", count)


if __name__ == "__main__":
    main()