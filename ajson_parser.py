import ply.yacc as yacc
from ajson_lexer import LexerClass

class Parser():
    tokens = LexerClass.tokens

    def __init__(self):
        self.parser = yacc.yacc(module=self)
        self.per = None

    def p_ajson(self, p):
        ''' ajson : LBRACKET contents RBRACKET
                | LBRACKET RBRACKET
        '''
        p[0] = p[2] if len(p) == 4 else None
        lista = []
        lista.append(p[0])
        self.per = lista

    def p_contents(self, p):
        ''' contents : key DOS_PUNTOS value opcional
                     | key DOS_PUNTOS value COMA contents
        '''
        p[0] = {p[1]: p[3]}
        if len(p) > 5:
            p[0].update(p[5])

    def p_opcional(self, p):
        ''' opcional : COMA
                     |
        '''
    def p_key(self, p):
        ''' key : STR_CON_COMILLAS
                | STR_SIN_COMILLAS
        '''
        p[0] = p[1]

    def p_value(self, p):
        ''' value : ajson
                  | operation
                  | NUMBER
                  | other
                  | arrayobjects
        '''
        p[0] = p[1]

    def p_arrayobjects(self,p):
        ''' arrayobjects : LCORCHETE valores RCORCHETE
                        | LCORCHETE RCORCHETE
        '''
        p[0] = p[2] if len(p) == 4 else None

    def p_valores(self, p):
        ''' valores : ajson opcional
                    | ajson COMA valores
        '''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_operation(self, p):
        ''' operation : menor
                    | mayor
                    | igual
                    | mayigual
                    | menigual'''
        p[0] = p[1]

    def p_menor(self, p):
        ''' menor : NUMBER MENOR NUMBER'''
        p[0] = p[1] < p[3]

    def p_mayor(self, p):
        ''' mayor : NUMBER MAYOR NUMBER'''
        p[0] = p[1] > p[3]

    def p_igual(self, p):
        ''' igual : NUMBER IGUAL NUMBER'''
        p[0] = p[1] == p[3]

    def p_mayigual(self, p):
        ''' mayigual : NUMBER MAYIGUAL NUMBER'''
        p[0] = p[1] >= p[3]

    def p_menigual(self, p):
        ''' menigual : NUMBER MENIGUAL NUMBER'''
        p[0] = p[1] <= p[3]


    def p_other(self, p):
        ''' other : TR
                  | FL
                  | NULL
                  | STR_CON_COMILLAS
        '''
        p[0] = p[1]
        if p[0] == "TR":
            p[0] = True
        elif p[0] == "FL":
            p[0] = False
        elif p[0] == "NULL":
            p[0]=None


    def p_error(self, p):
        print("Yacc error at", p)

    def unpack_item(self, key, value, prefix=""):
        items = []
        if isinstance(value, dict):
            for k, v in value.items():
                items.extend(self.unpack_item(k, v, f"{prefix}{key}."))
        elif isinstance(value, list):
            for index, item in enumerate(value):
                items.extend(self.unpack_item(index, item, f"{prefix}{key}."))
        else:
            key = key.strip('"') if isinstance(key, str) else key
            value = value.strip('"') if isinstance(value, str) else value
            items.append(f"{prefix}{key}: {value}")
        return items

    def unpack_dict(self, dictionary):
        return [item for key, value in dictionary.items() for item in self.unpack_item(key, value)]

    def unpack_list(self, lista):
        return [item for index, item in enumerate(lista) for item in self.unpack_item(index, item)]

    def test(self, data):
        self.parser.parse(data)
        items = []
        for key, value in self.per[0].items():
            items.extend(self.unpack_item(key, value))
        for item in items:
            print("{" + item + "}")
