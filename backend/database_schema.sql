-- Script SQL para criar as tabelas necessarias

-- Tabela de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    foto VARCHAR(255),
    telefone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de funcionarios
CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    foto VARCHAR(255),
    eh_barbeiro BOOLEAN DEFAULT FALSE,
    eh_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela da empresa (registro unico)
CREATE TABLE IF NOT EXISTS empresa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    endereco TEXT,
    cnpj VARCHAR(18) UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insere a empresa padrao caso ainda nao exista
INSERT INTO empresa (nome, descricao, endereco, cnpj, telefone, email)
SELECT 'Minha Barbearia', 'Barbearia moderna com os melhores profissionais.', 'Rua Exemplo, 123 - Centro', '00.000.000/0001-00', '(00) 00000-0000', 'contato@minhabarbearia.com'
WHERE NOT EXISTS (SELECT 1 FROM empresa);

-- Tabela de horarios de funcionamento
CREATE TABLE IF NOT EXISTS horarios_funcionamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana TINYINT NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),  -- 0 = Segunda, 6 = Domingo
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    UNIQUE KEY uq_dia_semana (dia_semana)
);

-- Tabela de agendamentos
CREATE TABLE IF NOT EXISTS agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    inicio DATETIME NOT NULL,
    fim DATETIME NOT NULL,
    cliente_id INT NOT NULL,
    barbeiro_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pendente',
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (barbeiro_id) REFERENCES funcionarios(id) ON DELETE CASCADE,
    INDEX idx_cliente (cliente_id),
    INDEX idx_barbeiro (barbeiro_id),
    INDEX idx_inicio (inicio),
    INDEX idx_fim (fim)
);

-- Tabela de historico de acessos de usuarios
CREATE TABLE IF NOT EXISTS acessos_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo_usuario ENUM('cliente', 'funcionario') NOT NULL,
    email VARCHAR(255) NOT NULL,
    data_hora_acesso DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_usuario_tipo (usuario_id, tipo_usuario),
    INDEX idx_data_hora_acesso (data_hora_acesso),
    INDEX idx_tipo_usuario (tipo_usuario)
);
