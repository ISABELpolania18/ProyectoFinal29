-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 25-06-2025 a las 02:45:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

-- SETS DE CONFIGURACIÓN (comentados para evitar errores en phpMyAdmin)
-- SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;
-- SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;
-- SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;
-- SET NAMES utf8mb4;

--
-- Base de datos: `filesbank`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_medicos`
--

CREATE TABLE `archivos_medicos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(50) NOT NULL,
  `cod_archivo` INT(100) NOT NULL,
  `Nombre_Paciente` VARCHAR(100) NOT NULL,
  `ID_Paciente` INT(50) NOT NULL,
  `Edad_Paciente` INT(10) NOT NULL,
  `Ruta_Dicom` VARCHAR(200) NOT NULL,
  `Ruta_Nifti` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_otros`
--

CREATE TABLE `archivos_otros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(50) NOT NULL,
  `cod_archivo` INT(100) NOT NULL,
  `tipo_archivo` ENUM('csv','mat','jpg','png') NOT NULL,
  `nombre_archivo` VARCHAR(100) NOT NULL,
  `fecha_archivo` DATE NOT NULL,
  `ruta_archivo` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre_usuario` VARCHAR(50) NOT NULL,
  `Contraseña` VARCHAR(100) NOT NULL,
  `Tipo_Usuario` ENUM('Imágenes','Señales') NOT NULL,
  PRIMARY KEY (`nombre_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`nombre_usuario`, `Contraseña`, `Tipo_Usuario`) VALUES
('juanita', '123', 'Imágenes'),
('pepito', '123', 'Señales');

COMMIT;

-- RESTAURAR CONFIGURACIONES (también comentadas para evitar errores)
-- SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
-- SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
-- SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
