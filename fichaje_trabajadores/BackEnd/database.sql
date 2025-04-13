
CREATE TABLE fitxatge_neteja (
    id_fitxatge INT AUTO_INCREMENT PRIMARY KEY,
    id_treballador INT NOT NULL,
    id_comunitat INT NOT NULL,
    tipus_fitxatge ENUM('i', 'o') NOT NULL,  -- 'i' para entrada, 'o' para salida
    data DATE NOT NULL,  -- Formato Día/Mes/Año
    hora TIME NOT NULL,  -- Hora en formato HH:MM:SS
    --- FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador),
    --- FOREIGN KEY (id_comunitat) REFERENCES comunitats(id_comunitat)
);

CREATE TABLE usuaris(
    tipus_usuari ENUM('admin','treballador','vei') NOT NULL,
    tipus_permis ENUM('baix','mitja','alt') NOT NULL
);

CREATE TABLE treballadors (
    id_treballador INT AUTO_INCREMENT PRIMARY KEY,
    nom_i_cognom VARCHAR(255) NOT NULL,
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL,
    correu VARCHAR(255) NOT NULL UNIQUE,
    contrasenya VARCHAR(255) NOT NULL
);

CREATE TABLE admins (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    nom_i_cognom VARCHAR(255) NOT NULL,
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL,
    correu VARCHAR(255) NOT NULL UNIQUE,
    contrasenya VARCHAR(255) NOT NULL
);

CREATE TABLE veins (
    id_vei INT AUTO_INCREMENT PRIMARY KEY,
    id_comunitat INT NO NULL
);

CREATE TABLE comunitats (
    id_comunitat INT AUTO_INCREMENT PRIMARY KEY,
    adreca VARCHAR(255) NOT NULL,
    latitud DECIMAL(9, 6) NOT NULL,  -- Latitud con precisión de 6 decimales
    longitud DECIMAL(9, 6) NOT NULL, -- Longitud con precisión de 6 decimales (s'hauria d'adaptar al num de decimals que extraiem de l'api del maps)
    ciutat VARCHAR(100) NOT NULL,
    codi_postal VARCHAR(10) NOT NULL,
    data_alta_empresa DATE NOT NULL,  -- Fecha de alta de la empresa
    data_alta_app DATE NOT NULL  -- Fecha de alta en la app
);

CREATE TABLE comunitat_placa_asignada (
    id_comunitat INT AUTO_INCREMENT PRIMARY KEY,
    placa_num INT NO NULL
);

CREATE TABLE places (
    placa_num INT AUTO_INCREMENT PRIMARY KEY,  -- Número de la plaza, que se autoincrementa
    id_treballador INT NOT NULL,  -- Referencia al trabajador que está asociado a la plaza
    departament ENUM('parkings', 'comunitats', 'oficines') NOT NULL -- Departamento al que pertenece la plaza
    --- FOREIGN KEY (id_treballador) REFERENCES treballadors(id_treballador)  -- Clave foránea que referencia la tabla treballadors
);

CREATE TABLE geolocalitzacio (
    id_fitxatge INT -- aquesta hauria de ser FOREIGN KEY perquè fa referencia a la de FITXATGE_NETEJA
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6)
);


CREATE TABLE incidencies (
    id_incidencia INT AUTO_INCREMENT,
    tipus_incidencia ENUM ('1','2','3','4'), -- INT CHECK (tipus_incidencia IN (1, 2, 3, 4)) valida. En canvi enum genera error si sintrodueix un parametre fora dels predefinits
    id_comunitat INT,
    id_treballador INT,
    nom_img VARCHAR(255),
    data DATE,
    hora TIME,
    temps_en_gestionar INT
);


CREATE TABLE tipus_incidencia (
    id_tipus INT AUTO_INCREMENT PRIMARY KEY,
    descripcio VARCHAR(255),
    temps_estimat_resoldre_incidencia INT
)

---taules sense primary key porque no se ha especificado una columna que se considere única y que sirva para identificar de forma única cada fila de la tabla.

CREATE TABLE calendari_any (
    id_treballador INT,
    id_comunitat INT,
    data DATE,
    ordre INT
);

CREATE TABLE calendari_amb_festiu_actualitzat (
    id_treballador INT,
    id_comunitat INT,
    data DATE,
    ordre INT
);

CREATE TABLE festius (
    data_festiu DATE,
    poblacio VARCHAR(255),
    codi_postal VARCHAR(10)
);

CREATE TABLE setmana (
    dia_setmana ENUM ('L','M','X','J','V'),
    tipus_treball ENUM ('E', 'V'),
    id_comunitat INT,
    ordre_comunitat INT
);
