import pickle


def read_file(name_file):
    with open(name_file, 'r', encoding="utf-8") as fln:
        text = fln.readlines()
    return text


def write_file(name_file, text):
    with open(name_file, 'w', encoding="utf-8") as fln:
        fln.writelines(text)


def add_file(name_file, text):
    with open(name_file, 'a', encoding="utf-8") as fln:
        fln.writelines(text)


def error_file(name_file):
    print("Фаил отсутствует в директории.")
    fl = open(name_file, 'w', encoding="utf-8")
    fl.close()
    print("Фаил успешно создан. Заполните его данными и перезапустите программу.")


def read_file_pickle(name_file):
    with open(name_file, 'rb') as fln:
        restored_data = pickle.load(fln)
    return restored_data


def write_file_pickle(name_file, data):
    with open(name_file, 'wb') as fln:
        pickle.dump(data, fln)


def error_file_pickle(name_file):
    print("Фаил отсутствует в директории.")
    fl = open(name_file, 'wb')
    fl.close()
    print("Фаил успешно создан. Заполните его данными и перезапустите программу.")



