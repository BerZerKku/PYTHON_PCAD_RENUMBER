# -*- coding: cp1251 -*-

# Замеченные ошибки: 
# исправлено 1. в PCAD перемеименование самого в себя вызывает ошибку

def getRefDes(ref):
    ''' (str) -> str

        Из полученного позиционного обозначения ref вырезается первая
        последовательность букв.

        Функция возвращает имя поз.обозначения

        >>> getRefDes('123R45')
        >>> "R"
        >>> getRefDes('R212')
        >>> "R"
        >>> getRefDes('C123A')
        >>> "C"
    '''
    global name

    # убираем спереди все символы, до появления первой буквы
    ref_tmp = ref
    for c in ref:
        if not c.isalpha():
            ref_tmp = ref_tmp.replace(c, '', 1)
        else:
            break
    ref = ref_tmp
    
    # оставим только последовательность букв
    ref_tmp = ""
    for c in ref:
        if c.isalpha():
            ref_tmp += c
        else:
            break

    return ref_tmp

def main(source):
    # откроем .bom файл на чтение, а .eco на запись
    f_bom = open(source, 'r')
    f_eco = open(source.replace('.bom', '.eco'), 'w')

    # в .eco файл запишем первые две строчки
    f_eco.write('; P-CAD 2006 Schematic Version 19.02.9589\n')
    f_eco.write('\n')
    
    # найдем строку с 'RefDes' и пропустим после нее еще две
    line = f_bom.readline()
    while not 'RefDes' in line:
        line = f_bom.readline()
    line = f_bom.readline()
    line = f_bom.readline()

    # считаем имеющиеся в файле поз.обозначения
    ref_list = []
    for line in f_bom.readlines():
        ref_list.append(line.split()[0])
    
    # (поз.обоз) -> (текущий индекс)
    name_dict = {}
    # (старое поз.обозначение) -> (новое поз.обозначение)
    new_ref_des = {}
    
    # сформируем новые имена
    while len(ref_list) > 0:
        # извлечем текущее имя
        ref = ref_list.pop(0)
        new_ref_des[ref] = ''
        tmp = getRefDes(ref)

        # при необходимости добавим новое поз.обозначние в
        # в список имеющихся и присвоим начальный индекс 1
        if not (tmp in name_dict):
            name_dict[tmp] = 1

        # найдем незанятое имя 
        new_ref = tmp + str(name_dict[tmp])
        name_dict[tmp] += 1
        while new_ref in ref_list:
            new_ref = tmp + str(name_dict[tmp])
            name_dict[tmp] += 1      
        new_ref_des[ref] = new_ref

    # сформируем записи для .eco файла
    for r in new_ref_des:
        # добавим только измененные поз.обозначения
        if r != new_ref_des[r]:
            line = 'RefdesChange ' + '"' + r + '" "' + new_ref_des[r] + '"\n'
            f_eco.write(line)
                    
    f_bom.close()
    f_eco.close()

if __name__ == '__main__':
    main('KPRD_021.bom')
    pass
