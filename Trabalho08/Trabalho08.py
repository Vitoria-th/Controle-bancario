from datetime import date

class Conta():
  def __init__(self, nroConta, nome, limite, senha):   
    self.__nroConta = nroConta
    self.__nome = nome
    self.__limite = limite
    self.__senha = senha
    self.__transacoes=[]

  def getNroConta(self):
    return self.__nroConta
    
  def getNome(self):
    return self.__nome
    
  def getLimite(self):
    return self.__limite

  def getSenha(self):
    return self.__senha

  def getTransacoes(self):
    return self.__transacoes
    
  def adicionaDeposito(self, valor, data, nomeDepositante):
    dep = Deposito(valor, data, nomeDepositante)
    self.__transacoes.append(dep)

  def adicionaSaque(self, valor, data, senha):
    if senha == self.__senha and (self.calculaSaldo() + self.__limite) >= valor:
      saq = Saque(valor, data, senha)
      self.__transacoes.append(saq)
    else:
      return False

  def adicionaTransf(self, valor, data, senha, contaFavorecido):
    if senha == self.__senha and (self.calculaSaldo() + self.__limite) >= valor:
      transf = Transferencia(valor, data, senha, "D")
      transf2 = Transferencia(valor, data, senha, "C")
        
      self.__transacoes.append(transf)
      contaFavorecido.getTransacoes().append(transf2)
    else:
      return False

  def calculaSaldo(self):
      saldofinal = 0
      for a in self.__transacoes:
         if type(a) is Saque:
           saldofinal = saldofinal - a.getValor()
         if type(a) is Deposito:
           saldofinal = saldofinal + a.getValor()
         if type(a) is Transferencia:
           if a.getTipoTransf() == "C":
            saldofinal = saldofinal + a.getValor()
           else:
            saldofinal = saldofinal - a.getValor()

      return saldofinal + self.__limite

class Transacao():
  def __init__(self, valor, data):
    self.__valor = valor
    self.__data = data

  def getValor(self):
    return self.__valor

  def getData(self):
    return self.__data

class Saque(Transacao):
  def __init__(self, valor, data,senha):
    super().__init__(valor, data)
    self.__senha = senha

  def getSenha(self):
    return self.__senha

class Transferencia(Transacao):
  def __init__(self, valor, data, senha, tipoTransf):
    super().__init__(valor, data)
    self.__senha = senha
    self.__tipoTransf = tipoTransf

  def getSenha(self):
    return self.__senha

  def getTipoTransf(self):
    return self.__tipoTransf

class Deposito(Transacao):
  def __init__(self, valor, data, nomeDepositante):
    super().__init__(valor, data)
    self.__nomeDepositante = nomeDepositante

  def getNomeDepositante(self):
    return self.__nomeDepositante



if __name__ == "__main__":
  c1 = Conta(1234, 'Jose da Silva', 1000, 'senha1')
  c1.adicionaDeposito(5000, date.today(), 'Antonio Maia')
  if c1.adicionaSaque(2000, date.today(), 'senha1') == False:
    print('Não foi possível realizar o saque no valor de 2000')
  if c1.adicionaSaque(1000, date.today(), 'senha-errada') == False: # deve falhar
    print('Não foi possível realizar o saque no valor de 1000')
 
  c2 = Conta(4321, 'Joao Souza', 1000, 'senha2')
  c2.adicionaDeposito(3000, date.today(), 'Maria da Cruz')
  if c2.adicionaSaque(1500, date.today(), 'senha2') == False:
    print('Não foi possível realizar o saque no valor de 1500')
  if c2.adicionaTransf(5000, date.today(), 'senha2', c1) == False: # deve falhar
    print('Não foi possível realizar a transf no valor de 5000')
  if c2.adicionaTransf(800, date.today(), 'senha2', c1) == False:
    print('Não foi possível realizar a transf no valor de 800') 
  print('--------')
  print('Saldo de c1: {}'.format(c1.calculaSaldo())) # deve imprimir 4800
  print('Saldo de c2: {}'.format(c2.calculaSaldo())) # deve imprimir 1700
