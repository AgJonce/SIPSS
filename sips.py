import streamlit as st
import locale
import sqlite3
import pandas as pd
import os
from datetime import datetime
import pytz
from datetime import date
import plotly.express as px
from urllib.parse import quote
from streamlit_calendar import calendar

# Cria pasta "data" se não existir
os.makedirs("data", exist_ok=True)

def criar_banco():
    conn = sqlite3.connect("data/banco.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL,
            email TEXT NOT NULL,
            nascimento TEXT NOT NULL,
            observacoes TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            duracao INTEGER NOT NULL,
            preco REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            servico_id INTEGER,
            data_hora TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (servico_id) REFERENCES servicos(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS financeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            pagamento TEXT NOT NULL,
            observacao TEXT
        )
    ''')
    conn.commit()
    conn.close()
def finalizar_servico(conn, id_agendamento, valor, servico_nome):
    import datetime

    cursor = conn.cursor()

    # Data atual
    data_finalizacao = datetime.datetime.now().isoformat()

    # Atualiza o status do agendamento
    cursor.execute("""
        UPDATE agendamentos
        SET status = 'Concluído'
        WHERE id = ?
    """, (id_agendamento,))

    # Lança no financeiro
    cursor.execute("""
        INSERT INTO financeiro (data, descricao, tipo, valor, categoria, pagamento, observacao)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data_finalizacao,
        f"Serviço finalizado: {servico_nome}",
        "Entrada",
        valor,
        "Serviço",
        "Não informado",
        None
    ))

    conn.commit()
    
def format_brl(valor):
    # Formata número em moeda brasileira com vírgula decimal
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Cria banco somente se não existir
if not os.path.exists("data/banco.db"):
    criar_banco()

conn = sqlite3.connect("data/banco.db", check_same_thread=False)
cursor = conn.cursor()

st.set_page_config(page_title="SIPS — Sistema Integrado de Prestação de Serviços", layout="centered")
st.title("📅 SIPS — Sistema Integrado de Prestação de Serviços!")

menu = [
    "🏠 Início",
    "👤 Cliente",
    "🔧 Serviço",
    "📇 Agendar",
    "📅 Agendamentos",
    "💰 Financeiro",
    "📊 Dashboard"
]

escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "🏠 Início":
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>👋 Bem-vindo ao <b>SIPS</b> — Sistema Integrado de Prestação de Serviços!</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center;">
        <img src="https://images.unsplash.com/photo-1556740749-887f6717d7e4?auto=format&fit=crop&w=800&q=80" width="500" style="border-radius: 15px;"/>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### O que você pode fazer no SIPS:
    - 📇 **Gerenciar clientes:** cadastre, edite e controle seus clientes facilmente.
    - 🛠️ **Gerenciar serviços:** mantenha seu catálogo de serviços sempre atualizado.
    - 📅 **Agendar serviços:** crie agendamentos rápidos e receba confirmações.
    - 📊 **Visualizar agendamentos:** acompanhe todos os seus compromissos em um só lugar.
    - 💰 **Controle financeiro:** registre entradas e saídas automaticamente.
    - 📈 **Dashboard interativo:** gráficos para entender melhor seus negócios.
    """)

    st.markdown("---")

    st.markdown("## 📰 Últimas notícias e dicas para empreendedores")
    st.markdown("""
    - [5 Dicas para Pequenos Negócios Crescerem em 2025](https://www.example.com/noticia1)  
      Aprenda estratégias simples para impulsionar seu negócio e aumentar as vendas.
    - [Como Fidelizar Clientes e Aumentar a Receita](https://www.example.com/noticia2)  
      Entenda a importância da experiência do cliente e como criar um relacionamento duradouro.
    - [Tendências de Mercado para o Setor de Serviços](https://www.example.com/noticia3)  
      Fique por dentro das novidades que vão movimentar o mercado este ano.
    """)

    st.markdown("---")

    st.markdown("## 🎥 Vídeos recomendados sobre Empreendedorismo")

    col1, col2 = st.columns(2)

    with col1:
        st.video("https://www.youtube.com/watch?v=znz7ibyObhA")  # Exemplo vídeo motivacional
        st.caption("Como começar um negócio do zero - Dicas essenciais")

    with col2:
        st.video("https://www.youtube.com/watch?v=nKW8tvM3mSc")  # Exemplo vídeo de gestão
        st.caption("Como Organizar o Financeiro de Sua Empresa")

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; margin-top: 20px;">
        <a href="mailto:support@sips.com" style="
            background-color: #4CAF50; 
            color: white; 
            padding: 10px 25px; 
            border-radius: 8px; 
            text-decoration: none; 
            font-weight: bold;
            font-size: 16px;">
            📩 Contate o Suporte
        </a>
    </div>
    """, unsafe_allow_html=True)


elif escolha == "👤 Cliente":
    st.header("Gestão de Clientes")
    # código cliente aqui
# e assim por diante...


    col1, col2, col3, col4 = st.columns(4)

    if "acao_cliente" not in st.session_state:
        st.session_state.acao_cliente = "incluir"

    with col1:
        if st.button("➕ Incluir"):
            st.session_state.acao_cliente = "incluir"

    with col2:
        if st.button("✏️ Alterar"):
            st.session_state.acao_cliente = "alterar"

    with col3:
        if st.button("🗑️ Excluir"):
            st.session_state.acao_cliente = "excluir"

    with col4:
        if st.button("🔍 Localizar"):
            st.session_state.acao_cliente = "localizar"

    acao = st.session_state.acao_cliente

    if acao == "incluir":
        st.markdown("### ➕ Incluir Novo Cliente")
        with st.form("form_incluir", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome completo")
                telefone = st.text_input("Telefone com DDD")
                cpf = st.text_input("CPF")
                email = st.text_input("Email")
            with col2:
                endereco = st.text_input("Endereço")
                nascimento = st.date_input(
                    "Data de nascimento",
                        value=date(2000, 1, 1),
                        max_value=date.today(),
                        format="DD/MM/YYYY")
                observacoes = st.text_area("Observações")
            enviado = st.form_submit_button("Salvar Cliente")
            if enviado:
                if nome and telefone and cpf and endereco and email:
                    cursor.execute("""
                        INSERT INTO clientes (nome, telefone, cpf, endereco, email, nascimento, observacoes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (nome, telefone, cpf, endereco, email, nascimento.isoformat(), observacoes))
                    conn.commit()
                    st.success(f"Cliente **{nome}** cadastrado com sucesso!")
                else:
                    st.warning("Preencha todos os campos obrigatórios.")

    elif acao == "alterar":
        st.markdown("### ✏️ Alterar Cliente")
        clientes = cursor.execute("SELECT id, nome FROM clientes").fetchall()
        cliente_dict = {c[1]: c[0] for c in clientes}
        selecao = st.selectbox("Selecione o cliente", list(cliente_dict.keys()))
    
        if selecao:
            id_cliente = cliente_dict[selecao]
            cliente = cursor.execute("SELECT * FROM clientes WHERE id=?", (id_cliente,)).fetchone()

            with st.form("form_servico", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    nome = st.text_input("Nome completo", cliente[1])
                    telefone = st.text_input("Telefone com DDD", cliente[2])
                    cpf = st.text_input("CPF", cliente[3])
                    email = st.text_input("Email", cliente[5])
                with col2:
                    endereco = st.text_input("Endereço", cliente[4])
                    nascimento = st.date_input(
                    "Data de nascimento",
                        value=date(2000, 1, 1),
                        max_value=date.today(),
                        format="DD/MM/YYYY")
                    observacoes = st.text_area("Observações", cliente[7])
                atualizado = st.form_submit_button("Atualizar Cliente")
                if atualizado:
                    cursor.execute("""
                        UPDATE clientes SET nome=?, telefone=?, cpf=?, endereco=?, email=?, nascimento=?, observacoes=?
                        WHERE id=?
                    """, (nome, telefone, cpf, endereco, email, nascimento.isoformat(), observacoes, id_cliente))
                    conn.commit()
                    st.success("Cliente atualizado com sucesso!")
    elif acao == "excluir":
        st.markdown("### 🗑️ Excluir Cliente")
        clientes = cursor.execute("SELECT id, nome FROM clientes").fetchall()
        cliente_dict = {c[1]: c[0] for c in clientes}
        selecao = st.selectbox("Selecione o cliente para excluir", list(cliente_dict.keys()))

        if selecao:
            id_cliente = cliente_dict[selecao]
            cliente = cursor.execute("SELECT * FROM clientes WHERE id=?", (id_cliente,)).fetchone()

            with st.form("form_servico", clear_on_submit=True):
                st.write(f"**Nome:** {cliente[1]}")
                st.write(f"**Telefone:** {cliente[2]}")
                st.write(f"**Email:** {cliente[5]}")
                confirmar = st.form_submit_button("Confirmar Exclusão")
                if confirmar:
                    cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
                    conn.commit()
                    st.success("Cliente excluído com sucesso!")
    elif acao == "localizar":
        st.markdown("### 🔍 Localizar Cliente")
        termo = st.text_input("Digite o nome ou parte do nome para buscar")
        if termo:
            resultados = cursor.execute("SELECT nome, telefone, email FROM clientes WHERE nome LIKE ?", ('%' + termo + '%',)).fetchall()
            if resultados:
                df_result = pd.DataFrame(resultados, columns=["Nome", "Telefone", "Email"])
                st.dataframe(df_result)
            else:
                st.info("Nenhum cliente encontrado.")
elif escolha == "🔧 Serviço":
    st.subheader("🔧 Novo Serviço")
    with st.form("form_servico", clear_on_submit=True):
        nome_serv = st.text_input("Nome do Serviço")
        duracao = st.number_input("Duração (minutos)", min_value=5, max_value=300, step=5)
        preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
        salvar = st.form_submit_button("Salvar Serviço")
        if salvar:
            if nome_serv and duracao > 0 and preco >= 0:
                cursor.execute("INSERT INTO servicos (nome, duracao, preco) VALUES (?, ?, ?)",
                            (nome_serv, duracao, preco))
                conn.commit()
                st.success(f"Serviço **{nome_serv}** cadastrado com sucesso!")
            else:
                st.warning("Preencha todos os campos corretamente.")

elif escolha == "📇 Agendar":
    st.subheader("📌 Novo Agendamento")

    # Busca clientes e serviços (id, nome, preco)
    clientes = cursor.execute("SELECT id, nome FROM clientes").fetchall()
    servicos = cursor.execute("SELECT id, nome, preco FROM servicos").fetchall()

    if not clientes or not servicos:
        st.warning("Cadastre clientes e serviços antes de agendar.")
    else:
        with st.form("form_agendamento", clear_on_submit=True):
            cliente_dict = {c[1]: c[0] for c in clientes}
            servico_dict = {s[1]: {"id": s[0], "preco": s[2]} for s in servicos}

            cliente_nomes = ["Selecione um cliente..."] + list(cliente_dict.keys())
            servico_nomes = ["Selecione um serviço..."] + list(servico_dict.keys())

            cliente_nome = st.selectbox("Cliente", cliente_nomes)
            servico_nome = st.selectbox("Serviço", servico_nomes)

            data = st.date_input("Data", value=datetime.today())
            hora = st.time_input("Hora")
            pagamento = st.selectbox("📈 Tipo", ["Selecione um Tipo...", "Pix", "Dinheiro","Cartão"])
            observacoes = st.text_area("Observações")
            enviar = st.form_submit_button("Agendar")

            if enviar:
                if cliente_nome.startswith("Selecione") or servico_nome.startswith("Selecione"):
                    st.warning("Por favor, selecione um cliente e um serviço.")
                else:
                    cliente_id = cliente_dict[cliente_nome]
                    servico_id = servico_dict[servico_nome]["id"]
                    servico_preco = servico_dict[servico_nome]["preco"]
                    data_hora = datetime.combine(data, hora).isoformat()

                    # Insere agendamento
                    cursor.execute("""
                        INSERT INTO agendamentos (cliente_id, servico_id, data_hora, observacoes)
                        VALUES (?, ?, ?, ?)
                    """, (cliente_id, servico_id, data_hora, observacoes))
                    conn.commit()

                    # Insere lançamento financeiro automático
                    cursor.execute("""
                        INSERT INTO financeiro (data, descricao, tipo, valor, categoria, pagamento, observacao)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data.isoformat(),
                        f"Agendamento automático: {servico_nome}"
                        "Entrada",
                        "Serviço",
                        servico_preco,
                         "Serviço",
                        "Não informado",
                        None
                    ))
                    conn.commit()

                    # Mensagem whatsapp
                    tel = cursor.execute("SELECT telefone FROM clientes WHERE id=?", (cliente_id,)).fetchone()[0]
                    msg = f"Olá! Seu agendamento de {servico_nome} está confirmado para {data} às {hora}."
                    link = f"https://wa.me/55{tel}?text={quote(msg)}"

                    st.success("Agendamento criado com sucesso! Lançamento financeiro registrado.")
                    st.markdown(f"[📲 Enviar confirmação no WhatsApp]({link})", unsafe_allow_html=True)

elif escolha == "📅 Agendamentos":
    st.subheader("📅 Calendário de Agendamentos")

    query = '''
        SELECT a.id, a.data_hora, c.nome AS cliente, s.nome AS servico
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN servicos s ON a.servico_id = s.id
    '''
    df = pd.read_sql_query(query, conn)

    if not df.empty:
        # Define fuso horário de Brasília
        tz_brasilia = pytz.timezone("America/Sao_Paulo")

        # Converte para datetime e aplica fuso horário
        df["start"] = pd.to_datetime(df["data_hora"], utc=True).dt.tz_convert("America/Sao_Paulo")
        df["end"] = df["start"] + pd.Timedelta(minutes=30)
        df["title"] = df["cliente"] + " - " + df["servico"]

        df["start"] = df["start"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        df["end"] = df["end"].dt.strftime("%Y-%m-%dT%H:%M:%S")

        eventos = df[["id", "title", "start", "end"]].to_dict("records")

        calendar_options = {
            "initialView": "dayGridMonth",
            "locale": "pt-br",  # ✅ Isso define o idioma como português
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay"
            },
            "selectable": True
        }

        calendar_data = calendar(events=eventos, options=calendar_options)

        if calendar_data and calendar_data.get("dateClick"):
            dia_selecionado = calendar_data["dateClick"]["date"][:10]
            st.markdown(f"### 📅 Agendamentos em {dia_selecionado}")

            agendamentos_dia = df[df["start"].str.startswith(dia_selecionado)][["start", "cliente", "servico"]]
            if not agendamentos_dia.empty:
                for i, row in agendamentos_dia.iterrows():
                    hora = pd.to_datetime(row["start"]).strftime("%H:%M")
                    st.markdown(f"- 🕒 {hora} - 👤 **{row['cliente']}** - 💼 {row['servico']}")
            else:
                st.info("Nenhum agendamento neste dia.")
    else:
        st.info("Nenhum agendamento registrado.")

elif escolha == "💰 Financeiro":
    st.subheader("💰 Controle Financeiro de Prestadores de Serviço")

    # Função para carregar dados do banco
    def carregar_financeiro():
        df = pd.read_sql_query("SELECT * FROM financeiro", conn)
        if not df.empty:
            df["data"] = pd.to_datetime(df["data"])
        return df

    # Carrega os serviços cadastrados para a categoria
    def carregar_categorias_servicos():
        df_servicos = pd.read_sql_query("SELECT nome FROM servicos", conn)
        return df_servicos["nome"].tolist()


    # Carrega dados para exibição
    df_financeiro = carregar_financeiro()
    categorias_servicos = carregar_categorias_servicos()

    with st.form("form_financeiro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input("📅 Data", value=datetime.today())
            tipo = st.selectbox("📈 Tipo", ["Selecione um Tipo...", "Entrada", "Saída"])
            categoria = st.selectbox("🏷️ Categoria (Serviço)", ["Selecione um Serviço..."] + categorias_servicos)
            pagamento = st.selectbox("📈 Tipo", ["Selecione um Tipo...", "Pix", "Dinheiro","Cartão"])
        with col2:
            descricao = st.text_input("📝 Descrição")
            valor = st.number_input("💰 Valor (R$)", min_value=0.01, format="%.2f")
            observacao = st.text_area("🗒️ Observação (opcional)", height=80)

        enviado = st.form_submit_button("💾 Salvar Lançamento")

        if enviado:
            if tipo == "Selecione um Tipo...":
                st.error("❗ Selecione um tipo válido.")
            elif categoria == "Selecione um Serviço...":
                st.error("❗ Selecione uma categoria válida.")
            elif not descricao:
                st.error("❗ Por favor, preencha a descrição.")
            elif valor <= 0:
                st.error("❗ Valor deve ser maior que zero.")
            else:
                cursor.execute("""
                    INSERT INTO financeiro (data, descricao, tipo, valor, categoria, pagamento, observacao)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (data.isoformat(),
                      descricao,
                      tipo,
                      valor,
                      categoria,
                      "Não informado",
                      observacao
                    ))
                conn.commit()
                st.success("✅ Lançamento salvo com sucesso!")
                df_financeiro = carregar_financeiro()
    st.write("### 🔍 Filtrar Lançamentos")
    if not df_financeiro.empty:
        df = df_financeiro.copy()

        data_min = df["data"].min().date()
        data_max = df["data"].max().date()
        dt_inicio, dt_fim = st.date_input("Período", [data_min, data_max])

        dt_inicio_ts = pd.to_datetime(dt_inicio)
        dt_fim_ts = pd.to_datetime(dt_fim)

        df = df[(df["data"] >= dt_inicio_ts) & (df["data"] <= dt_fim_ts)]
        df_display = df.sort_values(by="data", ascending=False).reset_index(drop=True)
        busca = st.text_input("🔎 Buscar na descrição")
        if busca:
            df = df[df["descricao"].str.contains(busca, case=False, na=False)]

        for index, row in df_display.iterrows():
            with st.expander(f"📌 {row['data'].strftime('%d/%m/%Y')} - {row['descricao']} ({row['tipo']})"):
                st.write(f"💰 Valor: R$ {row['valor']:,.2f}")
                st.write(f"🏷️ Categoria: {row['categoria']}")
                if row["observacao"]:
                    st.write(f"🗒️ Observação: {row['observacao']}")

        excluir_idx = st.number_input(
            "🗑️ Índice para excluir",
            min_value=0,
            max_value=len(df_display) - 1 if len(df_display) > 0 else 0,
            step=1
        )
        if st.button("Excluir lançamento"):
            id_excluir = df_display.loc[excluir_idx, "id"]
            cursor.execute("DELETE FROM financeiro WHERE id=?", (id_excluir,))
            conn.commit()
            st.success(f"🗑️ Lançamento índice {excluir_idx} excluído!")
            df_financeiro = carregar_financeiro()

        entradas = df[df["tipo"] == "Entrada"]["valor"]
        saidas = df[df["tipo"] == "Saída"]["valor"]

        total_entradas = entradas.sum()
        total_saidas = saidas.sum()
        saldo = total_entradas - total_saidas

        maior_entrada = entradas.max() if not entradas.empty else 0
        maior_saida = saidas.max() if not saidas.empty else 0
        media_entrada = entradas.mean() if not entradas.empty else 0
        media_saida = saidas.mean() if not saidas.empty else 0

        st.markdown("### 📊 Resumo Financeiro")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="💵 Total Entradas", value=f"R$ {total_entradas:,.2f}")
        col2.metric(label="💸 Total Saídas", value=f"R$ {total_saidas:,.2f}")
        col3.metric(label="💰 Saldo Atual", value=f"R$ {saldo:,.2f}")

        st.markdown("---")

        col4, col5, col6 = st.columns(3)
        col4.metric(label="⬆️ Maior Entrada", value=f"R$ {maior_entrada:,.2f}")
        col5.metric(label="⬇️ Maior Saída", value=f"R$ {maior_saida:,.2f}")
        col6.metric(label="📊 Média Entrada / Saída", value=f"R$ {media_entrada:,.2f} / R$ {media_saida:,.2f}")

        resumo = df.groupby(["categoria", "tipo"]).agg(
            Total_Valor=("valor", "sum"),
            Quantidade=("valor", "count"),
            Media_Valor=("valor", "mean")
        ).reset_index()

        st.markdown("### 📋 Resumo por Categoria e Tipo")
        for _, row in resumo.iterrows():
            with st.expander(f"🏷️ {row['categoria']} - {row['tipo']}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Total", f"R$ {row['Total_Valor']:,.2f}")
                col2.metric("🔢 Quantidade", row['Quantidade'])
                col3.metric("📊 Média", f"R$ {row['Media_Valor']:,.2f}")

        st.markdown("### 📈 Entradas e Saídas por Categoria")
        resumo_pivot = resumo.pivot(index="categoria", columns="tipo", values="Total_Valor").fillna(0)
        fig_cat = px.bar(
            resumo_pivot,
            barmode='group',
            labels={"value": "Valor (R$)", "categoria": "Categoria"}
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("### 📉 Evolução do Saldo")
        df_sorted = df.sort_values(by="data")
        df_sorted["Valor Ajustado"] = df_sorted.apply(
            lambda x: x["valor"] if x["tipo"] == "Entrada" else -x["valor"], axis=1
        )
        df_sorted["Saldo Acumulado"] = df_sorted["Valor Ajustado"].cumsum()
        fig_saldo = px.line(
            df_sorted, x="data", y="Saldo Acumulado",
            title="Saldo Acumulado ao longo do tempo",
            labels={"Saldo Acumulado": "Saldo (R$)", "data": "Data"}
        )
        st.plotly_chart(fig_saldo, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar lançamentos filtrados para CSV",
            data=csv, file_name='lancamentos_financeiros.csv', mime='text/csv'
        )
    else:
        st.info("ℹ️ Nenhum lançamento cadastrado ainda.")
        
elif escolha == "📊 Dashboard":
    st.subheader("📊 Dashboard")

    # Carregar dados financeiros diretamente do banco
    df_financeiro = pd.read_sql_query("SELECT * FROM financeiro", conn)
    if not df_financeiro.empty:
        df_financeiro["data"] = pd.to_datetime(df_financeiro["data"])
    else:
        df_financeiro = pd.DataFrame(columns=["id", "data", "descricao", "tipo", "valor", "categoria", "observacao"])

    # Carregar dados de agendamentos
    query_agend = """
        SELECT a.id, a.data_hora, c.nome AS cliente, s.nome AS servico
        FROM agendamentos a
        JOIN clientes c ON a.cliente_id = c.id
        JOIN servicos s ON a.servico_id = s.id
    """
    df_agend = pd.read_sql_query(query_agend, conn)
    if not df_agend.empty:
        df_agend["data_hora"] = pd.to_datetime(df_agend["data_hora"])
        df_agend["data"] = df_agend["data_hora"].dt.date

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💼 Financeiro")

        if df_financeiro.empty:
            st.info("Nenhum dado financeiro registrado.")
        else:
            # Resumo financeiro
            total_entradas = df_financeiro.loc[df_financeiro["tipo"] == "Entrada", "valor"].sum()
            total_saidas = df_financeiro.loc[df_financeiro["tipo"] == "Saída", "valor"].sum()
            saldo = total_entradas - total_saidas

            st.metric("💵 Total Entradas", f"R$ {total_entradas:,.2f}")
            st.metric("💸 Total Saídas", f"R$ {total_saidas:,.2f}")
            st.metric("💰 Saldo Atual", f"R$ {saldo:,.2f}")

            # Gráfico pizza de Entradas vs Saídas
            fig_pie = px.pie(
                df_financeiro.groupby("tipo")["valor"].sum().reset_index(),
                names="tipo",
                values="valor",
                title="Distribuição Financeira"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Gráfico barras por categoria e tipo
            resumo_cat = df_financeiro.groupby(["categoria", "tipo"])["valor"].sum().reset_index()
            resumo_pivot = resumo_cat.pivot(index="categoria", columns="tipo", values="valor").fillna(0)
            fig_bar = px.bar(
                resumo_pivot,
                barmode="group",
                title="Entradas e Saídas por Categoria",
                labels={"value": "Valor (R$)", "categoria": "Categoria"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("📆 Agendamentos")

        if df_agend.empty:
            st.info("Nenhum agendamento registrado.")
        else:
            # Agendamentos por data
            ag_count = df_agend.groupby("data").size().reset_index(name="Total")
            fig_bar_agend = px.bar(
                ag_count,
                x="data",
                y="Total",
                title="Total de Agendamentos por Dia",
                labels={"data": "Data", "Total": "Agendamentos"}
            )
            st.plotly_chart(fig_bar_agend, use_container_width=True)

            # Serviços mais agendados
            serv_count = df_agend["servico"].value_counts().reset_index()
            serv_count.columns = ["Serviço", "Quantidade"]
            fig_bar_serv = px.bar(
                serv_count.head(10),
                x="Serviço",
                y="Quantidade",
                title="Top 10 Serviços Mais Agendados",
                labels={"Quantidade": "Número de Agendamentos"}
            )
            st.plotly_chart(fig_bar_serv, use_container_width=True)
