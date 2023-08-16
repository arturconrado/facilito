CREATE TABLE rateio (
    Concurso INT,
    Data DATE,
    Faixa INT,
    Ganhadores INT,
    Premio DOUBLE PRECISION,
    PRIMARY KEY (Concurso, Faixa),
    FOREIGN KEY (Concurso) REFERENCES resultado (Concurso)
);