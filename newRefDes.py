# -*- coding: cp1251 -*-

# ���������� ������: 
# ���������� 1. � PCAD ���������������� ������ � ���� �������� ������

def getRefDes(ref):
    ''' (str) -> str

        �� ����������� ������������ ����������� ref ���������� ������
        ������������������ ����.

        ������� ���������� ��� ���.�����������

        >>> getRefDes('123R45')
        >>> "R"
        >>> getRefDes('R212')
        >>> "R"
        >>> getRefDes('C123A')
        >>> "C"
    '''
    global name

    # ������� ������� ��� �������, �� ��������� ������ �����
    ref_tmp = ref
    for c in ref:
        if not c.isalpha():
            ref_tmp = ref_tmp.replace(c, '', 1)
        else:
            break
    ref = ref_tmp
    
    # ������� ������ ������������������ ����
    ref_tmp = ""
    for c in ref:
        if c.isalpha():
            ref_tmp += c
        else:
            break

    return ref_tmp

def main(source):
    # ������� .bom ���� �� ������, � .eco �� ������
    f_bom = open(source, 'r')
    f_eco = open(source.replace('.bom', '.eco'), 'w')

    # � .eco ���� ������� ������ ��� �������
    f_eco.write('; P-CAD 2006 Schematic Version 19.02.9589\n')
    f_eco.write('\n')
    
    # ������ ������ � 'RefDes' � ��������� ����� ��� ��� ���
    line = f_bom.readline()
    while not 'RefDes' in line:
        line = f_bom.readline()
    line = f_bom.readline()
    line = f_bom.readline()

    # ������� ��������� � ����� ���.�����������
    ref_list = []
    for line in f_bom.readlines():
        ref_list.append(line.split()[0])
    
    # (���.����) -> (������� ������)
    name_dict = {}
    # (������ ���.�����������) -> (����� ���.�����������)
    new_ref_des = {}
    
    # ���������� ����� �����
    while len(ref_list) > 0:
        # �������� ������� ���
        ref = ref_list.pop(0)
        new_ref_des[ref] = ''
        tmp = getRefDes(ref)

        # ��� ������������� ������� ����� ���.���������� �
        # � ������ ��������� � �������� ��������� ������ 1
        if not (tmp in name_dict):
            name_dict[tmp] = 1

        # ������ ��������� ��� 
        new_ref = tmp + str(name_dict[tmp])
        name_dict[tmp] += 1
        while new_ref in ref_list:
            new_ref = tmp + str(name_dict[tmp])
            name_dict[tmp] += 1      
        new_ref_des[ref] = new_ref

    # ���������� ������ ��� .eco �����
    for r in new_ref_des:
        # ������� ������ ���������� ���.�����������
        if r != new_ref_des[r]:
            line = 'RefdesChange ' + '"' + r + '" "' + new_ref_des[r] + '"\n'
            f_eco.write(line)
                    
    f_bom.close()
    f_eco.close()

if __name__ == '__main__':
    main('KPRD_021.bom')
    pass
