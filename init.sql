-- Criação da tabela Cupcake
CREATE TABLE IF NOT EXISTS Cupcake (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco NUMERIC(10,2) NOT NULL,
    disponibilidade BOOLEAN DEFAULT TRUE,
    ingredientes TEXT,
    peso NUMERIC(5,2),
    dimensoes VARCHAR(50),
    informacoesNutricionais TEXT
);

-- Inserção de bolinhos de exemplo
INSERT INTO Cupcake (nome, descricao, preco, disponibilidade, ingredientes, peso, dimensoes, informacoesNutricionais)
VALUES
('Brigadeiro Gourmet', 'Bolinho recheado com brigadeiro caseiro e cobertura de granulado', 7.50, true, 'chocolate, leite condensado, granulado', 120.00, '5x5x6 cm', '250 kcal por unidade'),
('Red Velvet', 'Bolinho vermelho com cobertura de cream cheese', 8.00, true, 'cacau, cream cheese, corante alimentício', 110.00, '5x5x6 cm', '230 kcal por unidade'),
('Limão Siciliano', 'Bolinho de limão com cobertura de merengue suíço', 7.00, true, 'limão siciliano, farinha, açúcar, ovos', 115.00, '5x5x6 cm', '220 kcal por unidade'),
('Doce de Leite com Nozes', 'Bolinho recheado com doce de leite e pedaços de nozes', 8.50, true, 'doce de leite, nozes, farinha, ovos', 125.00, '5x5x6 cm', '270 kcal por unidade'),
('Vegano de Cacau', 'Bolinho vegano com massa de cacau e cobertura de ganache vegetal', 7.80, true, 'cacau, óleo de coco, açúcar mascavo, leite vegetal', 110.00, '5x5x6 cm', '210 kcal por unidade'),
('Diet de Morango', 'Bolinho diet recheado com morango e adoçado com xilitol', 9.00, true, 'morango, farinha integral, ovos, xilitol', 115.00, '5x5x6 cm', '200 kcal por unidade');