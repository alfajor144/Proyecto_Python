
INSERT INTO `usuario_usuario` (`id_usuario`, `nombre`, `apellido`, `contrasenia`, `email`, `cv`, `isAdmin`) VALUES ('0', 'Carlos', 'Balbiani', '1234', 'Carlos@gmail.com', NULL, '0');

INSERT INTO `usuario_usuario` (`id_usuario`, `nombre`, `apellido`, `contrasenia`, `email`, `cv`, `isAdmin`) VALUES ('1', 'Julio', 'Arrieta', '1234', 'Julio@gmail.com', NULL, '0');

INSERT INTO `usuario_usuario` (`id_usuario`, `nombre`, `apellido`, `contrasenia`, `email`, `cv`, `isAdmin`) VALUES ('2', 'Joaquin', 'Suarez', '1234', 'Joaquin@gmail.com', NULL, '0');

INSERT INTO `usuario_usuario` (`id_usuario`, `nombre`, `apellido`, `contrasenia`, `email`, `cv`, `isAdmin`) VALUES ('3', 'Juan', 'Juan', '1234', 'Admin@gmail.com', NULL, '1');


INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('0', 'Ayudante para AAD - IESTA ', 'Perfil: El llamado está dirigido a estudiantes avanzados de la Licenciatura en Estadística - Perfil Actuarial, preferentemente que hayan culminado tercer año.\r\nFacultad de Ciencias Económicas y de Administración, Av. Gonzalo Ramírez 1926, Sección Concursos (lunes a viernes de 10:00 a 13:00 horas, excepto el día de cierre en que solamente se reciben inscripciones hasta la hora 12:00)', 'Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19437');

INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('1', 'SUPLENTE AUX. DE ENFERMERÍA ', 'Requisitos: Ser ciudadano/a Natural o Legal.Título de Auxiliar de Enfermería habilitado y registrado en el M.S.P.Haber prestado Juramento de Fidelidad a la Bandera Nacional.Currículum Vitae con documentación probatoria foliado (méritos y antecedentes).No tener antecedentes funcionales negativos, provenientes de cualquier Entidad Pública yque revistan gravedad (al momento de la contratación).','Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19433');

INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('2', 'AMPLIACION SUPLENTE MEDICO ', 'Ser ciudadano/a Natural o Legal.Título de Médico Anestesista registrado y habilitado por el M.S.P. Currículum Vitae con documentación probatoria foliada (méritos y antecedentes).Acreditar inscripción vigente en el Colegio de Médicos del Uruguay(Ley N.º 18.591 – Art. 2º)No tener antecedentes funcionales negativos provenientes de cualquier Entidad Pública y que revistan gravedad (al momento de la contratación).','Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19429');

INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('3', 'Auxiliar de Enfermería habilitado', 'Perfil: El llamado está dirigido a estudiantes avanzados de la Licenciatura en Estadística - Perfil Actuarial, preferentemente que hayan culminado tercer año.\r\nFacultad de Ciencias Económicas y de Administración, Av. Gonzalo Ramírez 1926, Sección Concursos (lunes a viernes de 10:00 a 13:00 horas, excepto el día de cierre en que solamente se reciben inscripciones hasta la hora 12:00)','Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19437');

INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('4', 'SUPLENTE ciudadano DE ENFERMERÍA ', 'Requisitos: Ser ciudadano/a Natural o Legal.Título de Auxiliar de Enfermería habilitado y registrado en el M.S.P.Haber prestado Juramento de Fidelidad a la Bandera Nacional.Currículum Vitae con documentación probatoria foliado (méritos y antecedentes).No tener antecedentes funcionales negativos, provenientes de cualquier Entidad Pública yque revistan gravedad (al momento de la contratación).','Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19433');

INSERT INTO `usuario_oferta` (`id_oferta`, `titulo`, `descripcion`, `pais`, `fecha_inicio`, `fecha_final`, `link`) VALUES ('5', 'Médico Anestesista registrado', 'Ser ciudadano/a Natural o Legal.Título de Médico Anestesista registrado y habilitado por el M.S.P. Currículum Vitae con documentación probatoria foliada (méritos y antecedentes).Acreditar inscripción vigente en el Colegio de Médicos del Uruguay(Ley N.º 18.591 – Art. 2º)No tener antecedentes funcionales negativos provenientes de cualquier Entidad Pública y que revistan gravedad (al momento de la contratación).','Uruguay', '2020-12-01', '2020-12-31', 'https://www.uruguayconcursa.gub.uy/Portal/servlet/com.si.recsel.verllamado?19429');


INSERT INTO `usuario_postulacion`(`id`, `fecha_uno`, `fecha_dos`, `fecha_tres`, `id_oferta_id`, `id_usuario_id`, `calificacion`) VALUES ('0', NULL, NULL, NULL, '0', '0', NULL);

INSERT INTO `usuario_postulacion`(`id`, `fecha_uno`, `fecha_dos`, `fecha_tres`, `id_oferta_id`, `id_usuario_id`, `calificacion`) VALUES ('1', NULL, NULL, NULL, '1', '1', NULL);

INSERT INTO `usuario_postulacion`(`id`, `fecha_uno`, `fecha_dos`, `fecha_tres`, `id_oferta_id`, `id_usuario_id`, `calificacion`) VALUES ('2', NULL, NULL, NULL, '2', '2', NULL);


INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('0','Administracion','0');

INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('1','Enfermeria','1');

INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('2','Medicina','2');

INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('3','Enfermeria','3');

INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('4','Enfermeria','4');

INSERT INTO `usuario_categoria`(`id`, `nombre`, `id_Oferta_id`) VALUES ('5','Medicina','5');

INSERT INTO `auth_user`(`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES ('0','pbkdf2_sha256$216000$zjNwm1zApvRa$qzLGJmoD7UfzxQIQXgXHgbJed88azJS9nALebOhyaTk=','','1','admin','','','admin@admin.com','1','1','2020-09-27 01:46:52.537069')
