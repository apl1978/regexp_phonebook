import csv
import re

REGEX = r"(\+7|8)?\s*[\(\-\s*]?(\d{3})[\)-]*\s*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*(\(*(доб.)\s*(\d+)\)*)?"
SUBST = "+7(\\2)\\3-\\4-\\5 \\7\\8"


def get_list_from_file():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        return list(rows)


def write_list_to_file(contacts_list):
    with open("phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


def converting_phonebook(contacts_list):
    for cont in contacts_list:
        if len(cont) > 7:
            del cont[7]
        phone = cont[-2]
        result = re.sub(REGEX, SUBST, phone).strip()
        cont[-2] = result
        list_lfs = ' '.join(cont[0:3]).split()
        cont[0] = list_lfs[0]
        cont[1] = list_lfs[1]
        if len(list_lfs) == 3:
            cont[2] = list_lfs[2]
    return contacts_list


def delete_doubles(contacts_list):
    list_for_delete = []
    for cont in contacts_list:
        for cont1 in contacts_list:
            if cont1[0] in cont and cont1[1] in cont and cont1 != cont:
                for i, val in enumerate(zip(cont, cont1)):
                    if val[0] != val[1]:
                        cont[i] = val[0] if val[0] != '' else val[1]
                if cont1 not in list_for_delete:
                    list_for_delete.append(cont1)

    for el in list_for_delete:
        contacts_list.remove(el)
    return contacts_list


if __name__ == '__main__':
    contacts_list = get_list_from_file()

    contacts_list = converting_phonebook(contacts_list)

    contacts_list = delete_doubles(contacts_list)

    write_list_to_file(contacts_list)
