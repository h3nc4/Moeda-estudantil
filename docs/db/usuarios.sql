CREATE OR REPLACE VIEW public.usuarios
 AS
 SELECT u.id AS user_id,
    u.last_login,
    u.username,
    u.is_active,
    u.date_joined,
    u.email,
    u.moedas,
    COALESCE(aluno.cpf, professor.cpf) AS cpf,
    aluno.rg,
    u.is_superuser AS is_admin,
    aluno.id AS aluno_id,
    empresa.id AS empresa_id,
    professor.id AS professor_id
   FROM logic_usuario u
     LEFT JOIN logic_aluno aluno ON u.aluno_id = aluno.id
     LEFT JOIN logic_empresa empresa ON u.empresa_id = empresa.id
     LEFT JOIN logic_professor professor ON u.professor_id = professor.id;
