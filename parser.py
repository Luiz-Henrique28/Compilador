# /home/runner/workspace/parser.py

from token_type import TokenType
from ast_nodes import (BinOp, Num, Var, Assign, VarDecl, BlockNode, IfNode,
                       WhileNode, StringNode, ProgramaNode, NoOp, TipoNode,
                       UnaryOp, EscritaNode)


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Token inesperado"):
        raise Exception(f"Erro de Sintaxe: {message} -> {self.current_token}")

    def eat(self, tipo_token):
        if self.current_token.tipo == tipo_token:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(
                f"Esperado {tipo_token}, mas encontrou {self.current_token.tipo}"
            )

    def fator(self):
        token = self.current_token
        if token.tipo == TokenType.MAIS:
            self.eat(TokenType.MAIS)
            return UnaryOp(token, self.fator())
        elif token.tipo == TokenType.MENOS:
            self.eat(TokenType.MENOS)
            return UnaryOp(token, self.fator())
        elif token.tipo == TokenType.INTEIRO_CONST:
            self.eat(TokenType.INTEIRO_CONST)
            return Num(token)
        elif token.tipo == TokenType.REAL_CONST:
            self.eat(TokenType.REAL_CONST)
            return Num(token)
        elif token.tipo == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            return self.variavel()

    def termo(self):
        node = self.fator()
        while self.current_token.tipo in (TokenType.MULT,
                                          TokenType.DIV_INTEIRA,
                                          TokenType.DIV_REAL):
            token = self.current_token
            if token.tipo == TokenType.MULT:
                self.eat(TokenType.MULT)
            elif token.tipo == TokenType.DIV_INTEIRA:
                self.eat(TokenType.DIV_INTEIRA)
            elif token.tipo == TokenType.DIV_REAL:
                self.eat(TokenType.DIV_REAL)
            node = BinOp(left=node, op=token, right=self.fator())
        return node

    def expr(self):
        node = self.termo()
        while self.current_token.tipo in (TokenType.MAIS, TokenType.MENOS):
            token = self.current_token
            if token.tipo == TokenType.MAIS:
                self.eat(TokenType.MAIS)
            elif token.tipo == TokenType.MENOS:
                self.eat(TokenType.MENOS)
            node = BinOp(left=node, op=token, right=self.termo())
        return node

    def declaracao(self):
        if self.current_token.tipo == TokenType.ID:
            return self.atribuicao()
        if self.current_token.tipo == TokenType.ESCREVA:
            return self.declaracao_escrita()
        # Adicionar outras declarações como SE, ENQUANTO, etc. aqui
        return NoOp()

    def declaracao_escrita(self):
        self.eat(TokenType.ESCREVA)
        self.eat(TokenType.LPAREN)
        node = EscritaNode(self.expr())
        self.eat(TokenType.RPAREN)
        return node

    def atribuicao(self):
        left = self.variavel()
        token = self.current_token
        self.eat(TokenType.ATRIBUICAO)
        right = self.expr()
        return Assign(left, token, right)

    def variavel(self):
        node = Var(self.current_token)
        self.eat(TokenType.ID)
        return node

    def tipo(self):
        token = self.current_token
        if token.tipo == TokenType.INTEIRO_TIPO:
            self.eat(TokenType.INTEIRO_TIPO)
        elif token.tipo == TokenType.REAL_TIPO:
            self.eat(TokenType.REAL_TIPO)
        return TipoNode(token)

    def declaracoes_variaveis(self):
        declaracoes = []
        if self.current_token.tipo == TokenType.VAR:
            self.eat(TokenType.VAR)
            while self.current_token.tipo == TokenType.ID:
                var_node = Var(self.current_token)
                self.eat(TokenType.ID)
                self.eat(TokenType.DOIS_PONTOS)
                tipo_node = self.tipo()
                declaracoes.append(VarDecl(var_node, tipo_node))
                self.eat(TokenType.PONTO_VIRGULA)
        return declaracoes

    def lista_declaracoes(self):
        nodes = [self.declaracao()]
        while self.current_token.tipo == TokenType.PONTO_VIRGULA:
            self.eat(TokenType.PONTO_VIRGULA)
            nodes.append(self.declaracao())

        # Checagem para garantir que não há um ID solto no final
        if self.current_token.tipo == TokenType.ID:
            self.error(
                "ID inesperado no final de uma declaração. Faltou um ';' ?")

        return nodes

    def bloco_principal(self):
        self.eat(TokenType.INICIO)
        nodes = self.lista_declaracoes()
        self.eat(TokenType.FIM)
        self.eat(TokenType.PONTO)
        return BlockNode(nodes)

    def programa(self):
        self.eat(TokenType.PROGRAMA)
        nome_programa = self.variavel()
        self.eat(TokenType.PONTO_VIRGULA)
        declaracoes_vars = self.declaracoes_variaveis()
        bloco_principal = self.bloco_principal()
        return ProgramaNode(nome_programa, declaracoes_vars, bloco_principal)

    def parse(self):
        node = self.programa()
        if self.current_token.tipo != TokenType.EOF:
            self.error("Código extra encontrado após o final do programa.")

        print("Análise sintática concluída com sucesso!")
        return node
