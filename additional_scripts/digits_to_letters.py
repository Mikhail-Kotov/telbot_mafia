def replace_digits_with_letters(input_number: int) -> str:
    return chr(65 + input_number)


# Пример использования
#input_string = "9"
for i in range(26):
    output_string = replace_digits_with_letters(i)
    print(output_string)
