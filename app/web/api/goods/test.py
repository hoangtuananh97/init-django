# import numpy as np
# # <class 'list'>: ['エ', 'カ', 'カ', 'サ', 'タ', 'ツ', 'テ', 'フ', 'ミ']
# katakana = ['ア', 'イ', 'ウ', 'エ', 'オ',
#             'カ', 'キ', 'ク', 'ケ', 'コ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ',
#             'サ', 'シ', 'ス', 'セ', 'ソ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ',
#             'タ', 'チ', 'ツ', 'テ', 'ト', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド',
#             'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',
#             'ハ', 'ヒ', 'フ', 'ヘ', 'ホ', 'バ', 'ビ', 'ブ', 'ベ', 'ボ',
#             'マ', 'ミ', 'ム', 'メ', 'モ', 'パ', 'ピ', 'ブ', 'ペ', 'ポ',
#             'ヤ', 'ユ', 'ヨ',
#             'ラ', 'リ', 'ル', 'レ', 'ロ',
#             'ワ', 'ヲ',
#             'ン', ]
#
# companies = ['メイダイシャ', 'テスト', 'ツジノー', 'ウメテスト', 'メイダイシャタカイテスト',
#              'メイダイシャテスト', 'チヨダコウギョウ', 'アキラコウキ']
#
#
# array_split_company_name = []
# for company in companies:
#     array_split_company_name.append(company[0])
#
# get_index_katakana = [katakana.index(company) for company in array_split_company_name]
#
# array_sort_split = [x for y, x in sorted(zip(get_index_katakana, array_split_company_name))]
# array_sort_companies = [x for _, x in sorted(zip(get_index_katakana,companies), key=lambda pair: pair[0])]
#
# print(array_sort_split)
# print(array_sort_companies)

import openpyxl as openpyxl


def readCsv(file):
    ex = openpyxl.load_workbook(file, read_only=True)
    sheet = ex.active
    arr_prefix = set()
    arr_gakubu = set()
    arr_name = set()
    arr_gakaka = []
    obj = {}


    for row in sheet.rows:
        prefix = row[8].value if row[8].value else ""
        if prefix not in ['prefix', 'name', 'division', 'gakka', 'gakubu', 'gakubu', 'hurigana', 'kind', 'bunri']:
            arr_prefix.add(prefix)

    for prefix in arr_prefix:
        arr = set()
        obj_1 = {}
        for row in sheet.rows:
            name = row[8].value if row[8].value else ""
            gakubu = row[4].value if row[4].value else ""
            if name not in ['prefix', 'name', 'division', 'gakka', 'gakubu', 'gakubu', 'hurigana', 'kind', 'bunri']:
                if name == prefix:
                    arr.add(gakubu)
        for ele in arr:
            obj_1['gakubu'] = ele
            obj_1['name'] = prefix
            arr_gakaka.append(obj_1)

            # if gakubu not in arr_gakubu and name not in arr_name:
            #     obj_1['gakubu'] = gakubu
            #     obj_1['name'] = name
            #     arr_gakaka.append(obj_1)
            #     arr_name.add(name)
            #     arr_gakubu.add(gakubu)
            # # arr_prefix.add(obj_1)


    for arr_gakaka_ele in arr_gakaka:
        arr = []
        for row in sheet.rows:
            name = row[8].value if row[8].value else ""
            gakubu = row[4].value if row[4].value else ""
            gakaka = row[5].value if row[5].value else ""
            if arr_gakaka_ele['name'] == name and arr_gakaka_ele['gakubu'] == gakubu:
                arr.append(gakaka)
        obj['{}:{}'.format(arr_gakaka_ele['name'], arr_gakaka_ele['gakubu'])] = set(arr)

    return obj


if __name__ == '__main__':
    json_division_1 = readCsv('file1.xlsx')
    # json_division_2 = readCsv('file2.xlsx')
    # json_division_3 = readCsv('file3.xlsx')
    # json_division_4 = readCsv('file4.xlsx')
    print(json_division_1)
    # print(json_division_2)
    # print(json_division_3)
    # print(json_division_4)
