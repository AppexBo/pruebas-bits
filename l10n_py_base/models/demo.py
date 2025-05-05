l10n_py_operacion_condition = {
        '1' : 'Contado',
        '2' : 'Crédito'
    }


def et(i = False):
    if not i:
        for k, v in l10n_py_operacion_condition.items():
            print(k,v)

    else:
        print(l10n_py_operacion_condition[i])

et('2')