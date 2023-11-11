CREATE OR REPLACE VIEW public.usuarios
 AS
 SELECT user.id AS user_id,
    user.last_login,
    user.is_superuser,
    user.username,
    user.is_active,
    user.date_joined,
    user.email,
    user.moedas,
    COALESCE(aluno.cpf, professor.cpf) AS cpf,
    aluno.rg,
    aluno.id AS aluno_id,
    empresa.id AS empresa_id,
    professor.id AS professor_id
   FROM logic_usuario user
     LEFT JOIN logic_aluno aluno ON user.aluno_id = aluno.id
     LEFT JOIN logic_empresa empresa ON user.empresa_id = empresa.id
     LEFT JOIN logic_professor professor ON user.professor_id = professor.id;

ALTER TABLE public.usuarios
    OWNER TO developer;
