CIVIL_CHOICES = (
    ('1', 'Solteiro(a)'),
    ('2', 'Casado(a)'),
    ('3', 'Divorciado(a)'),
    ('4', 'Viuvo(a)'),
    ('5', 'União Estável'),
    ('6', 'Outros'),
)

REGIME_CHOICES = (
    ('CLT', 'CLT'),
    ('PJ', 'PJ'),
    ('FREE', 'Free Lance'),
    ('PS', 'Prestação Serviços'),
    ('Outros', 'Outros'),
)

TURNO_CHOICES = (
    ('D', 'Diurno'),
    ('N', 'Noturno'),
)

PARENTESCO_CHOICES = (
    ('F', 'Filho(a)'),
    ('N', 'Neto(a)'),
    ('I', 'Irmão(a)'),
    ('O', 'Outro'),

)

TIPO_MEDICAMENTO_CHOICES = (
    ('1', 'Comprimido'),
    ('2', 'Cápsulas'),
    ('3', 'Creme'),
    ('4', 'Gotas'),
    ('5', 'Injeção Musc'),
    ('6', 'Injeção Subcutânea'),
    ('7', 'Injeção Venosa'),
    ('8', 'Pomada'),
    ('9', 'Solução'),
    ('10', 'Spray'),
    ('11', 'Supositório'),
    ('12', 'Outros'),
)

ESPECIALIDADE_CHOICES = (
    ('1', 'Alergista'),
    ('2', 'Cardiologia'),
    ('3', 'Clinico Geral'),
    ('4', 'Dermatologia'),
    ('5', 'Endocrinologia'),
    ('6', 'Fisiatria'),
    ('7', 'Fonoaudiologia'),
    ('8', 'Gastroenterologia'),
    ('9', 'Geriatria'),
    ('10', 'Ginecologia'),
    ('11', 'Nefrologia'),
    ('12', 'Neurologia'),
    ('13', 'Nutrição'),
    ('14', 'Obstetrícia'),
    ('15', 'Odontologia'),
    ('16', 'Oftalmologia'),
    ('17', 'Oncologia'),
    ('18', 'Ortopedia'),
    ('19', 'Otorrinolaringologia'),
    ('20', 'Pediatria'),
    ('21', 'Pneumologia'),
    ('22', 'Proctologia'),
    ('23', 'Psicologia'),
    ('24', 'Psiquiatria'),
    ('25', 'Reumatologia'),
    ('26', 'Traumatologia'),
    ('27', 'Urologia'),
    ('28', 'Outras'),


)

ATENDIMENTO_CHOICES = (
    ('1', 'Primeira'),
    ('2', 'Retorno-Exames'),
    ('3', 'Retorno'),
    ('4', 'Emergência'),
    ('5', 'Remoto')
)

CANCELAMENTO_CONSULTA_CHOICES = (
    ('1', 'A pedido do médico'),
    ('2', 'A pedido dos responsáveis'),
    ('3', 'Não é mais necessária'),
    ('4', 'Outros'),

)

POSOLOGIA_CHOICES = (
    ('1 vez ', '1 vez'),
    ('2 vezes ', '2 vezes'),
    ('3 vezes ', '3 vezes'),
    ('4 vezes ', '4 vezes'),
    ('5 vezes ', '5 vezes'),
    ('6 vezes ', '6 vezes'),
)

USO_CONTINUO_CHOICES = (
    ('Sim ', 'Sim'),
    ('Não ', 'Não'),
)

FORNECEDOR_PRINCIPAL_CHOICES = (
    ('1', 'Farmácia Hospital'),
    ('2', 'Farmácia Popular'),
    ('3', 'Farmácia - Drogaria'),
    ('4', 'Farmácia de Manipulação'),
    ('5', 'Drogaria - Site'),
    ('6', 'Mercado Livre'),
    ('7', 'Outros'),
)

REFEICAO_CHOICES = (
    ('1', 'Em jejum'),
    ('2', 'Após café da manhã'),
    ('3', 'Antes de almoçar'),
    ('4', 'Após almoço'),
    ('5', 'Antes do jantar'),
    ('6', 'Após jantar'),
    ('7', 'Antes de dormir'),
    ('8', 'Na madrugada'),
)

TIPO_INSULINA_CHOICES = (
    ('1', 'Lantus'),
    ('2', 'NovoRapid'),
    ('3', 'Nenhuma'),
)

TIPO_CONJUNTA_CHOICES = (
    ('1', 'sim'),
    ('2', 'Não'),
)

TIPO_CONTA_CHOICES = (
    ('1', 'Corrente'),
    ('2', 'Poupança'),
)

CREDITO_REF_CHOICES = (
    ('1', 'Salário'),
    ('2', 'Salário com 13º'),
    ('3', 'Reembolso'),
    ('4', 'Transferência entre contas'),
    ('5', 'Credito juros'),
    ('6', 'Outros'),
)

DESPESA_CHOICES = (
    ('1', 'Açougue'),
    ('2', 'Advogado'),
    ('3', 'Agropecuária -Ração e Medicamentos'),
    ('4', 'Água Mineral'),
    ('5', 'Caixa Cuidadores'),
    ('6', 'Combustível'),
    ('7', 'Conserto eletrodomésticos'),
    ('8', 'Consulta Medica'),
    ('9', 'Conta - Água'),
    ('10', 'Conta - Celular'),
    ('11', 'Conta - CPFL'),
    ('12', 'Conta - Funerária'),
    ('13', 'Conta - Carnê INSS'),
    ('14', 'Conta - Internet'),
    ('15', 'Conta - IPTU'),
    ('16', 'Conta - IPVA'),
    ('17', 'Conta - Luz'),
    ('18', 'Conta - Seguro'),
    ('19', 'Conta - Telefone Fixo'),
    ('20', 'Eletrodoméstico'),
    ('21', 'Exame'),
    ('22', 'Farmácia'),
    ('23', 'Gás de Cozinha'),
    ('24', 'Guia E-Social'),
    ('25', 'Impressões ou Cópias'),
    ('26', 'IOF de conta devedora'),
    ('27', 'Jardinagem'),
    ('28', 'Juros de conta devedora'),
    ('29', 'Leite'),
    ('30', 'Mão de Obra'),
    ('31', 'Material Conserto'),
    ('32', 'Material Construção'),
    ('33', 'Material Segurança'),
    ('34', 'Móveis'),
    ('35', 'Outros'),
    ('36', 'Padaria'),
    ('37', 'Pedágio'),
    ('38', 'Reembolso'),
    ('39', 'Roupas'),
    ('40', 'Salários Funcionários'),
    ('41', 'Saque'),
    ('42', 'Supermercado'),
    ('43', 'Utensílios domésticos'),
)

FORMA_PAGAMENTO_CHOICES = (
    ('1', 'Cheque'),
    ('2', 'Débito cartão'),
    ('3', 'Débitado em conta corrente'),
    ('4', 'Dinheiro'),

)
