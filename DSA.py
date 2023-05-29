import sys
import argparse
import pandas as pd
import numpy as np
import os.path as op

def dsa(path, dataset_name, href, mode_output=False, name_output='dataset.csv'):
    infodata = pd.DataFrame(columns=['Название набора данных', 'Ссылка на набор данных', 'Количество записей в наборе',
                                     'Количество столбцов в наборе', 'Общее количество пустых значений в наборе',
                                     'Количество пустых значений в каждом из столбцов',
                                     'Мин/макс/ср количество пустых значений в строке'])
    sheet = pd.read_csv(path, na_values=['None', '-'])
    rownum = len(sheet)  # количество записей в наборе
    colnum = len(sheet.columns)  # количество столбцов в наборе
    nannum = sheet.isna().sum().sum()  # общее количество пустых значений в наборе
    if nannum == 0:
        nancolnum = '0;0;0;0;0;0;0'
        minmaxmean = '0/0/0'
    else:
        nancolnum = sheet.isna().sum()
        strcol = ""
        for i in range(0, len(nancolnum)):
            strcol += str(nancolnum[i]) + ";"
        nancolnum = strcol[:len(strcol) - 1]  # количество пустых значений в каждом из столбцов( в виде строки через ;)
        minmaxmean = sheet.isna().sum(axis=1)
        minmaxmean.drop(np.where(minmaxmean < 1)[0], inplace=True)
        minmaxmean = str(minmaxmean.min()) + '/' + str(minmaxmean.max()) + '/' + str(round(minmaxmean.mean(), 2))  # мин/макс/ср пустых значений в строках
    infodata.loc[len(infodata.index)] = [dataset_name, href, rownum, colnum, nannum, nancolnum, minmaxmean]
    if mode_output:
        infodata.to_csv(name_output, mode='a', index=False, header=not op.exists(name_output), encoding='utf-8-sig')
    print("\n" + infodata.set_index('Название набора данных').transpose().to_string())


def parseargum():
    if len(sys.argv) < 2:
        print('Введите путь до набора данных формата csv:')
        path = input()
        print('Введите название набора данных:')
        dataset_name = input()
        print('Введите ссылку по которой находится набор данных:')
        href = input()
        print('Сохранить таблицу в файл csv?(Да/Нет)')
        if input() == "Да":
            mode = True
        else:
            mode = False
        name_output = 'dataset.csv'
    else:
        my_parser = argparse.ArgumentParser(description='Анализ качества данных')
        my_parser.add_argument('Path',
                           metavar='path',
                           type=str,
                           help='путь к файлу с набором данных csv формата')
        my_parser.add_argument('Dataset_name',
                           metavar='dataset_name',
                           type=str,
                           help='название набора данных')
        my_parser.add_argument('Href',
                           metavar='href',
                           type=str,
                           help='Ссылка на набор данных')
        my_parser.add_argument('-m',
                           '--Mode',
                           action='store_true',
                           help='Создавать или нет таблицу в файле формата csv')
        my_parser.add_argument('--name_output',
                           type=str,
                           default='dataset.csv',
                           help='Название создаваемой таблицы. По умолчанию dataset')
        args = my_parser.parse_args()
        path = args.Path
        dataset_name = args.Dataset_name
        href = args.Href
        mode = args.Mode
        name_output = args.name_output
    if not op.exists(path):
        print('Файл формата csv по заданному пути не существует')
        sys.exit()
    return path, dataset_name, href, mode, name_output


[path, dataset_name, href, mode, name_output] = parseargum()
dsa(path=path,
    dataset_name=dataset_name,
    href=href,
    mode_output=mode,
    name_output=name_output)
