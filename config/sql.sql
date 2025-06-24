CREATE TABLE tbl_aspirantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    curso ENUM('Full Stack', 'Data Science', 'Machine Learning', 'DevOps') NOT NULL,
    sexo ENUM('Masculino', 'Femenino', 'Otro') NOT NULL,
    habla_ingles BOOLEAN NOT NULL DEFAULT FALSE,
    imagen_perfil VARCHAR(255) DEFAULT NULL,
    archivo_pdf VARCHAR(255) DEFAULT NULL,
    aceptado BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
