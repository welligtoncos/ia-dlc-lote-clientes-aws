CREATE TABLE IF NOT EXISTS lotes (
    id               BIGINT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo     VARCHAR(255) NOT NULL,
    caminho_arquivo  VARCHAR(512) NULL,
    status           VARCHAR(20)  NOT NULL DEFAULT 'PENDENTE',
    total_linhas     INT          DEFAULT 0,
    linhas_validas   INT          DEFAULT 0,
    linhas_invalidas INT          DEFAULT 0,
    erro             TEXT,
    celery_task_id   VARCHAR(155),
    criado_em        DATETIME DEFAULT CURRENT_TIMESTAMP,
    concluido_em     DATETIME NULL
) ENGINE=InnoDB;
