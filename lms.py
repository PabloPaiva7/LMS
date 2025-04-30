import streamlit as st
from datetime import datetime

# Simulando "banco de dados" com session_state
if "cursos" not in st.session_state:
    st.session_state.cursos = {}  # {curso_id: {"nome": ..., "descricao": ...}}

if "alunos" not in st.session_state:
    st.session_state.alunos = {}  # {cpf: {"nome": ..., "email": ...}}

if "matriculas" not in st.session_state:
    st.session_state.matriculas = []  # [{"cpf": ..., "curso_id": ..., "data": ...}]

# Funções
def cadastrar_curso(curso_id, nome, descricao):
    if curso_id in st.session_state.cursos:
        st.warning("Curso já cadastrado.")
        return
    st.session_state.cursos[curso_id] = {"nome": nome, "descricao": descricao}
    st.success("Curso cadastrado com sucesso!")

def cadastrar_aluno(cpf, nome, email):
    if cpf in st.session_state.alunos:
        st.warning("Aluno já cadastrado.")
        return
    st.session_state.alunos[cpf] = {"nome": nome, "email": email}
    st.success("Aluno cadastrado com sucesso!")

def matricular_aluno(cpf, curso_id):
    for m in st.session_state.matriculas:
        if m["cpf"] == cpf and m["curso_id"] == curso_id:
            st.warning("Aluno já matriculado neste curso.")
            return
    st.session_state.matriculas.append({
        "cpf": cpf,
        "curso_id": curso_id,
        "data": datetime.now()
    })
    st.success("Matrícula realizada com sucesso!")

# Interface
st.title("🎓 Sistema LMS (Learning Management System)")

aba = st.sidebar.radio("Navegar para:", [
    "Cadastrar Curso", "Cadastrar Aluno", "Matrículas",
    "Listar Cursos", "Listar Alunos", "Histórico de Matrículas"
])

if aba == "Cadastrar Curso":
    st.header("📘 Cadastro de Curso")
    with st.form("form_curso"):
        curso_id = st.text_input("Código do Curso")
        nome = st.text_input("Nome do Curso")
        descricao = st.text_area("Descrição")
        if st.form_submit_button("Cadastrar"):
            cadastrar_curso(curso_id, nome, descricao)

elif aba == "Cadastrar Aluno":
    st.header("🧑‍🎓 Cadastro de Aluno")
    with st.form("form_aluno"):
        cpf = st.text_input("CPF do Aluno")
        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
        if st.form_submit_button("Cadastrar"):
            cadastrar_aluno(cpf, nome, email)

elif aba == "Matrículas":
    st.header("📝 Matrícula de Aluno")
    if not st.session_state.alunos or not st.session_state.cursos:
        st.warning("É necessário cadastrar alunos e cursos antes.")
    else:
        with st.form("form_matricula"):
            cpf = st.selectbox("Aluno", options=st.session_state.alunos.keys(), format_func=lambda cpf: st.session_state.alunos[cpf]["nome"])
            curso_id = st.selectbox("Curso", options=st.session_state.cursos.keys(), format_func=lambda cid: st.session_state.cursos[cid]["nome"])
            if st.form_submit_button("Matricular"):
                matricular_aluno(cpf, curso_id)

elif aba == "Listar Cursos":
    st.header("📚 Cursos Cadastrados")
    if not st.session_state.cursos:
        st.info("Nenhum curso cadastrado.")
    else:
        for cid, c in st.session_state.cursos.items():
            st.write(f"**{cid} - {c['nome']}**")
            st.caption(c['descricao'])

elif aba == "Listar Alunos":
    st.header("👨‍🏫 Alunos Cadastrados")
    if not st.session_state.alunos:
        st.info("Nenhum aluno cadastrado.")
    else:
        for cpf, a in st.session_state.alunos.items():
            st.write(f"**{cpf} - {a['nome']}** | {a['email']}")

elif aba == "Histórico de Matrículas":
    st.header("📜 Histórico de Matrículas")
    if not st.session_state.matriculas:
        st.info("Nenhuma matrícula registrada.")
    else:
        for m in st.session_state.matriculas[::-1]:
            aluno = st.session_state.alunos.get(m["cpf"], {})
            curso = st.session_state.cursos.get(m["curso_id"], {})
            st.write(f"{m['data'].strftime('%d/%m/%Y %H:%M')} | {aluno.get('nome')} matriculado em {curso.get('nome')}")

