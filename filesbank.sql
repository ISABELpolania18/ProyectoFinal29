-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-07-2025 a las 19:57:55
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `filesbank`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_medicos`
--

CREATE TABLE `archivos_medicos` (
  `nombre_usuario` varchar(50) NOT NULL,
  `cod_archivo` int(100) NOT NULL,
  `Nombre_Paciente` varchar(100) NOT NULL,
  `ID_Paciente` int(50) NOT NULL,
  `Edad_Paciente` int(10) NOT NULL,
  `Ruta_Dicom` varchar(200) NOT NULL,
  `Ruta_Nifti` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `archivos_otros`
--

CREATE TABLE `archivos_otros` (
  `nombre_usuario` varchar(50) NOT NULL,
  `cod_archivo` int(100) NOT NULL,
  `tipo_archivo` enum('csv','mat','jpg','png') NOT NULL,
  `nombre_archivo` varchar(100) NOT NULL,
  `fecha_archivo` date NOT NULL,
  `ruta_archivo` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `nombre_usuario` varchar(50) NOT NULL,
  `Contraseña` varchar(100) NOT NULL,
  `Tipo_Usuario` enum('Imágenes','Señales') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`nombre_usuario`, `Contraseña`, `Tipo_Usuario`) VALUES
('juanita', '123', 'Imágenes'),
('pepito', '123', 'Señales');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `archivos_medicos`
--
ALTER TABLE `archivos_medicos`
  ADD PRIMARY KEY (`nombre_usuario`);

--
-- Indices de la tabla `archivos_otros`
--
ALTER TABLE `archivos_otros`
  ADD PRIMARY KEY (`nombre_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`nombre_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
