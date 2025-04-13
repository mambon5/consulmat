-- 1. Comunitats (es referenciada por muchas)
CREATE TABLE comunitats (
    id_comunitat INT AUTO_INCREMENT PRIMARY KEY,
    adreca VARCHAR(255) NOT NULL,
    latitud DECIMAL(9, 6) NOT NULL,
    longitud DECIMAL(9, 6) NOT NULL,
    ciutat VARCHAR(100) NOT NULL,
    codi_postal VARCHAR(10) NOT NULL,
    data_alta_empresa DATE NOT NULL,
    data_alta_app TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Usuaris (no depende de nadie)
CREATE TABLE usuaris (
    tipus_usuari ENUM('admin','treballador','vei') NOT NULL,
    tipus_permis ENUM('baix','mitja','alt') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Treballadors (referencia comunitats)
CREATE TABLE treballadors (
    id_treballador INT AUTO_INCREMENT PRIMARY KEY,
    nom_i_cognom VARCHAR(255) NOT NULL,
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL,
    correu VARCHAR(255) NOT NULL UNIQUE,
    contrasenya VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 4. Admins (no referencia a nadie)
CREATE TABLE admins (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nom_i_cognom VARCHAR(255) NOT NULL,
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL,
    correu VARCHAR(255) NOT NULL UNIQUE,
    contrasenya VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Veïns (referencia comunitats)
CREATE TABLE veins (
    id_vei INT AUTO_INCREMENT PRIMARY KEY,
    id_comunitat INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 6. Comunitat_placa_asignada (indirectamente referencia comunitats y places)
CREATE TABLE comunitat_placa_asignada (
    id_comunitat INT NOT NULL,
    placa_num INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 7. Places (referencia treballadors)
CREATE TABLE places (
    placa_num INT AUTO_INCREMENT PRIMARY KEY,
    id_treballador INT NOT NULL,
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 8. Tipus_incidencia (sin dependencias)
CREATE TABLE tipus_incidencia (
    id_tipus INT AUTO_INCREMENT PRIMARY KEY,
    descripcio VARCHAR(255) NOT NULL,
    temps_estimat_resoldre_incidencia INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 9. Incidencies (referencia treballadors y comunitats)
CREATE TABLE incidencies (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    tipus_incidencia ENUM ('1','2','3','4') NOT NULL,
    id_comunitat INT NOT NULL,
    id_treballador INT NOT NULL,
    nom_img VARCHAR(255) NOT NULL,
    dataa DATE NOT NULL,
    hora TIME NOT NULL,
    temps_en_gestionar INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 10. Fitxatge_neteja (referencia treballadors y comunitats)
CREATE TABLE fitxatge_neteja (
    id_fitxatge INT AUTO_INCREMENT PRIMARY KEY,
    id_treballador INT NOT NULL,
    id_comunitat INT NOT NULL,
    tipus_fitxatge ENUM('i', 'o') NOT NULL,
    dataa DATE NOT NULL,
    hora TIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 11. Geolocalitzacio (referencia fitxatge_neteja)
CREATE TABLE geolocalitzacio (
    id_fitxatge INT NOT NULL,
    latitud DECIMAL(9,6) NOT NULL,
    longitud DECIMAL(9,6) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_fitxatge) REFERENCES fitxatge_neteja(id_fitxatge)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 12. Festius (sin referencias)
CREATE TABLE festius (
    data_festiu DATE NOT NULL,
    poblacio VARCHAR(255) NOT NULL,
    codi_postal VARCHAR(10) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (data_festiu, poblacio, codi_postal)
);

-- 13. Calendari_any (referencia treballadors y comunitats)
CREATE TABLE calendari_any (
    id_treballador INT NOT NULL,
    id_comunitat INT NOT NULL,
    dataa DATE NOT NULL,
    ordre INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_treballador, id_comunitat, dataa, ordre),
    FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 14. Calendari_amb_festiu_actualitzat (igual que la anterior)
CREATE TABLE calendari_amb_festiu_actualitzat (
    id_treballador INT NOT NULL,
    id_comunitat INT NOT NULL,
    dataa DATE NOT NULL,
    ordre INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_treballador, id_comunitat, dataa, ordre),
    FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- 15. Setmana (referencia comunitats)
CREATE TABLE setmana (
    dia_setmana ENUM ('L','M','X','J','V','S') NOT NULL,
    tipus_treball ENUM ('E', 'V') NOT NULL,
    id_comunitat INT NOT NULL,
    ordre_comunitat INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (dia_setmana, tipus_treball, id_comunitat, ordre_comunitat),
    FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
