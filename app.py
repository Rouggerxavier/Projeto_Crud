# app.py
import streamlit as st
import pandas as pd
from datetime import date
from conexao import conectar   # usa a MESMA conexão do seu projeto

# ================== CONFIG ==================
st.set_page_config(page_title="Sistema do Bar", layout="wide")
st.title("🍻 Sistema do Bar")

# ================== HELPERS ==================
def get_conn():
    return conectar()

def run_write(sql, params=None):
    conn = None
    try:
        conn = get_conn()
        with conn, conn.cursor() as cur:
            cur.execute(sql, params or ())
        return True, "ok"
    except Exception as e:
        return False, str(e)
    finally:
        if conn:
            conn.close()

def run_fetch_df(sql, params=None):
    conn = None
    try:
        conn = get_conn()
        return pd.read_sql(sql, conn, params=params)
    finally:
        if conn:
            conn.close()

def pick_id_from(df, label_col="nome", id_col="id", label_suffix=None):
    """
    Transforma DF em lista [(label, id_int)], retorna (default_id_int, options).
    Converte id para int nativo (evita numpy.int64).
    """
    if df.empty:
        return None, []
    options = []
    for _, r in df.iterrows():
        _id = r[id_col]
        try:
            _id = int(_id)
        except Exception:
            pass
        label = f"{r[label_col]} (#{_id})"
        try:
            if label_suffix and (label_suffix in r.index) and pd.notna(r[label_suffix]):
                label = f"{r[label_col]} - {r[label_suffix]} (#{_id})"
        except Exception:
            pass
        options.append((label, _id))
    return options[0][1], options

def select_id(label, options, key):
    if not options:
        return None
    labels = [o[0] for o in options]
    chosen = st.selectbox(label, labels, index=0, key=key)
    for text, _id in options:
        if text == chosen:
            try:
                return int(_id)
            except Exception:
                return _id
    return None

# ================== TABS ==================
tabs = st.tabs(["Clientes", "Produtos", "Vendedores", "Compras", "Relatórios"])

# ---------------------- CLIENTES ----------------------
with tabs[0]:
    st.subheader("Clientes")

    with st.expander("➕ Cadastrar cliente", expanded=True):
        cols = st.columns(3)
        nome = cols[0].text_input("Nome", key="cli_nome")
        telefone = cols[1].text_input("Telefone", key="cli_tel")
        email = cols[2].text_input("Email", key="cli_email")

        cols2 = st.columns(3)
        idade = cols2[0].number_input("Idade", min_value=0, step=1, key="cli_idade")
        cidade = cols2[1].text_input("Cidade", key="cli_cidade")
        torce = cols2[2].selectbox("Torce Flamengo?", ["Não", "Sim"], key="cli_torce") == "Sim"
        assiste = st.selectbox("Assiste One Piece?", ["Não", "Sim"], key="cli_assiste") == "Sim"

        if st.button("Salvar cliente", key="cli_salvar"):
            ok, msg = run_write("""
                INSERT INTO clientes (nome, telefone, email, idade, cidade, torce_flamengo, assiste_one_piece)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (nome, telefone, email, idade, cidade, torce, assiste))
            if ok:
                st.toast("Cliente salvo! ✅")
            else:
                st.error(msg)

    df_cli = run_fetch_df("""
        SELECT id, nome, telefone, email, idade, cidade,
               torce_flamengo AS flamengo, assiste_one_piece AS one_piece
        FROM clientes ORDER BY id
    """)
    st.dataframe(df_cli, use_container_width=True, height=320)

    with st.expander("📦 Pedidos do cliente selecionado"):
        if df_cli.empty:
            st.info("Sem clientes.")
        else:
            _, opts_cli_ped = pick_id_from(df_cli)
            csel = select_id("Cliente", opts_cli_ped, key="cli_hist_sel")
            if csel:
                df_hist = run_fetch_df("""
                    SELECT c.id, c.data_compra, c.total_bruto, c.desconto_total,
                           c.total_liquido, c.status, c.status_pagto
                    FROM compra c
                    WHERE c.cliente_id = %s
                    ORDER BY c.data_compra DESC
                """, (int(csel),))
                st.dataframe(df_hist, use_container_width=True, height=240)

    with st.expander("🗑️ Remover cliente"):
        if df_cli.empty:
            st.info("Sem clientes.")
        else:
            _, opts_cli_rm = pick_id_from(df_cli)
            cid_rm = select_id("Selecione o cliente", opts_cli_rm, key="cli_rm_sel")
            if st.button("Remover cliente selecionado", key="cli_rm_btn"):
                if cid_rm is None:
                    st.warning("Selecione um cliente.")
                else:
                    ok, msg = run_write("DELETE FROM clientes WHERE id=%s", (int(cid_rm),))
                    if ok:
                        st.toast("Cliente removido! 🗑️")
                    else:
                        st.error(msg)

# ---------------------- PRODUTOS ----------------------
with tabs[1]:
    st.subheader("Produtos")

    with st.expander("➕ Cadastrar produto", expanded=True):
        p1, p2, p3, p4 = st.columns(4)
        p_nome = p1.text_input("Nome do produto", key="prod_nome")
        p_preco = p2.number_input("Preço", min_value=0.0, step=0.5, format="%.2f", key="prod_preco")
        p_qtde  = p3.number_input("Quantidade", min_value=0, step=1, key="prod_qtde")
        p_tipo  = p4.selectbox("Tipo", ["", "bebida", "comida"], key="prod_tipo")
        p_origem = st.text_input("Origem (cidade)", key="prod_origem")

        if st.button("Salvar produto", key="prod_salvar"):
            ok, msg = run_write("""
                INSERT INTO produtos (nome, preco, quantidade, tipo, origem_cidade)
                VALUES (%s,%s,%s,%s,%s)
            """, (p_nome, p_preco, p_qtde, p_tipo if p_tipo else None, p_origem or None))
            if ok:
                st.toast("Produto salvo! ✅")
            else:
                st.error(msg)

    # Mostrar/ocultar inativos
    ver_inativos = st.checkbox("Mostrar produtos inativos", key="prod_ver_inativos")

    # 🔎 Filtros de busca
    with st.expander("🔎 Filtros de busca de produtos", expanded=False):
        f_nome = st.text_input("Nome contém", key="f_prod_nome")
        f_min  = st.number_input("Preço mínimo", min_value=0.0, step=0.5, format="%.2f", key="f_prod_min")
        f_max  = st.number_input("Preço máximo", min_value=0.0, step=0.5, format="%.2f", key="f_prod_max")
        f_tipo = st.selectbox("Tipo (categoria)", ["", "bebida", "comida"], key="f_prod_tipo")
        f_mari = st.checkbox("Somente fabricados em Mari", key="f_prod_mari")

    where = ["TRUE"] if ver_inativos else ["ativo = TRUE"]
    params = []

    if f_nome:
        where.append("LOWER(nome) LIKE LOWER(%s)")
        params.append(f"%{f_nome}%")
    if f_min and f_min > 0:
        where.append("preco >= %s")
        params.append(f_min)
    if f_max and f_max > 0:
        where.append("preco <= %s")
        params.append(f_max)
    if f_tipo:
        where.append("tipo = %s")
        params.append(f_tipo)
    if f_mari:
        where.append("origem_cidade ILIKE 'mari'")

    sql_prod = f"""
        SELECT id, nome, preco, quantidade, data_cadastro, tipo, origem_cidade, ativo
        FROM produtos
        WHERE {' AND '.join(where)}
        ORDER BY id
    """
    df_prod = run_fetch_df(sql_prod, tuple(params) if params else None)
    st.dataframe(df_prod, use_container_width=True, height=320)

    # Remover / Inativar
    with st.expander("🗑️ Remover / Inativar produto"):
        if df_prod.empty:
            st.info("Sem produtos na lista.")
        else:
            _, opts_prod_rm = pick_id_from(df_prod)
            pid_rm = select_id("Selecione o produto", opts_prod_rm, key="prod_rm_sel")

            col_rm1, col_rm2 = st.columns(2)

            if col_rm1.button("Remover produto selecionado", key="prod_rm_btn"):
                if pid_rm is None:
                    st.warning("Selecione um produto.")
                else:
                    # checa referências
                    df_ref = run_fetch_df("SELECT COUNT(*) AS qtd FROM item_compra WHERE produto_id=%s", (int(pid_rm),))
                    ref_count = int(df_ref.iloc[0]["qtd"])
                    if ref_count > 0:
                        st.warning(
                            f"Não é possível remover: este produto já foi usado em compras ({ref_count} registro/s). "
                            "Você pode inativá-lo para não aparecer mais nas vendas."
                        )
                    else:
                        ok, msg = run_write("DELETE FROM produtos WHERE id=%s", (int(pid_rm),))
                        if ok:
                            st.toast("Produto removido! 🗑️")
                        else:
                            st.error(msg)

            if col_rm2.button("Inativar produto selecionado", key="prod_inativar_btn"):
                if pid_rm is None:
                    st.warning("Selecione um produto.")
                else:
                    ok, msg = run_write("UPDATE produtos SET ativo=FALSE WHERE id=%s", (int(pid_rm),))
                    if ok:
                        st.toast("Produto inativado! 🚫")
                    else:
                        st.error(msg)

    # ===== Ajustar Estoque (entrada/saída/correção) =====
    with st.expander("📦 Ajustar estoque (entrada/saída/correção)"):
        df_prod_aj = run_fetch_df("""
            SELECT id, nome, quantidade
            FROM produtos
            WHERE ativo = TRUE
            ORDER BY nome
        """)
        if df_prod_aj.empty:
            st.info("Sem produtos ativos.")
        else:
            _, opts_prod_aj = pick_id_from(df_prod_aj, label_col="nome", id_col="id")
            pid_aj = select_id("Produto", opts_prod_aj, key="aj_prod")
            tipo_aj = st.radio("Tipo de ajuste", ["entrada","saida","correcao"], horizontal=True, key="aj_tipo")
            qtde_aj = st.number_input("Quantidade", min_value=1, step=1, key="aj_qtde")
            motivo_aj = st.text_input("Motivo (opcional)", key="aj_motivo")

            if st.button("Aplicar ajuste", key="aj_aplicar"):
                if pid_aj is None:
                    st.warning("Selecione um produto para ajustar.")
                else:
                    ok, msg = run_write("CALL ajustar_estoque(%s,%s,%s,%s)",
                                        (int(pid_aj), tipo_aj, int(qtde_aj), motivo_aj or None))
                    if ok:
                        st.toast("Estoque ajustado! 📦")
                    else:
                        st.error(msg)

        st.markdown("**Últimas movimentações**")
        df_mov = run_fetch_df("""
            SELECT m.id, p.nome, m.tipo, m.quantidade, m.motivo, m.criado_em
            FROM movimentacao_estoque m
            JOIN produtos p ON p.id = m.produto_id
            ORDER BY m.id DESC
            LIMIT 20
        """)
        st.dataframe(df_mov, use_container_width=True, height=240)

# ---------------------- VENDEDORES ----------------------
with tabs[2]:
    st.subheader("Vendedores (Garçons)")

    with st.expander("➕ Cadastrar vendedor", expanded=True):
        v1, v2, v3 = st.columns(3)
        v_nome = v1.text_input("Nome", key="vend_nome")
        v_cpf  = v2.text_input("CPF (11 dígitos)", key="vend_cpf")
        v_mat  = v3.text_input("Matrícula", key="vend_mat")

        v4, v5, v6 = st.columns(3)
        v_email  = v4.text_input("Email", key="vend_email")
        v_tel    = v5.text_input("Telefone", key="vend_tel")
        v_status = v6.selectbox("Status", ["ativo", "inativo", "ferias", "afastado"], key="vend_status")

        if st.button("Salvar vendedor", key="vend_salvar"):
            ok, msg = run_write("""
                INSERT INTO vendedor (nome, cpf, matricula, email, telefone, status)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (v_nome, v_cpf or None, v_mat or None, v_email or None, v_tel or None, v_status))
            if ok:
                st.toast("Vendedor salvo! ✅")
            else:
                st.error(msg)

    # Mostrar/ocultar inativos
    ver_vend_inativos = st.checkbox("Mostrar vendedores inativos", key="vend_ver_inativos")

    if ver_vend_inativos:
        df_vend = run_fetch_df("""
            SELECT id, nome, cpf, matricula, email, telefone, status, data_admissao, data_demissao, ativo
            FROM vendedor
            ORDER BY id
        """)
    else:
        df_vend = run_fetch_df("""
            SELECT id, nome, cpf, matricula, email, telefone, status, data_admissao, data_demissao, ativo
            FROM vendedor
            WHERE ativo = TRUE
            ORDER BY id
        """)
    st.dataframe(df_vend, use_container_width=True, height=320)

    with st.expander("🗑️ Remover / Inativar vendedor"):
        if df_vend.empty:
            st.info("Sem vendedores na lista.")
        else:
            _, opts_vend_rm = pick_id_from(df_vend)
            vid_rm = select_id("Selecione o vendedor", opts_vend_rm, key="vend_rm_sel")

            col_vrm1, col_vrm2 = st.columns(2)

            # Remover (só se não houver compras)
            if col_vrm1.button("Remover vendedor selecionado", key="vend_rm_btn"):
                if vid_rm is None:
                    st.warning("Selecione um vendedor.")
                else:
                    df_ref_v = run_fetch_df("SELECT COUNT(*) AS qtd FROM compra WHERE vendedor_id=%s", (int(vid_rm),))
                    ref_count_v = int(df_ref_v.iloc[0]["qtd"])
                    if ref_count_v > 0:
                        st.warning(
                            f"Não é possível remover: este vendedor está vinculado a {ref_count_v} compra(s). "
                            "Você pode inativá-lo para que não apareça mais nas telas de compra."
                        )
                    else:
                        ok, msg = run_write("DELETE FROM vendedor WHERE id=%s", (int(vid_rm),))
                        if ok:
                            st.toast("Vendedor removido! 🗑️")
                        else:
                            st.error(msg)

            # Inativar
            if col_vrm2.button("Inativar vendedor selecionado", key="vend_inativar_btn"):
                if vid_rm is None:
                    st.warning("Selecione um vendedor.")
                else:
                    ok, msg = run_write("UPDATE vendedor SET ativo=FALSE WHERE id=%s", (int(vid_rm),))
                    if ok:
                        st.toast("Vendedor inativado! 🚫")
                    else:
                        st.error(msg)

# ---------------------- COMPRAS ----------------------
with tabs[3]:
    st.subheader("Compras")

    # Auxiliares
    df_cli2  = run_fetch_df("SELECT id, nome, cidade FROM clientes ORDER BY nome")
    df_vend2 = run_fetch_df("SELECT id, nome FROM vendedor WHERE ativo = TRUE ORDER BY nome")
    df_forma = run_fetch_df("SELECT id, tipo FROM forma_pagto ORDER BY id")
    df_abertas = run_fetch_df("""
        SELECT id, cliente_id, vendedor_id, data_compra
        FROM compra WHERE status = 'aberto' ORDER BY id DESC
    """)

    # 1) Nova compra
    st.markdown("### 1) Nova compra")
    if df_cli2.empty or df_vend2.empty:
        st.info("Cadastre pelo menos 1 cliente e 1 vendedor para criar compras.")
    else:
        _, opts_cli_new = pick_id_from(df_cli2, label_col="nome", id_col="id", label_suffix="cidade")
        _, opts_vdd_new = pick_id_from(df_vend2, label_col="nome", id_col="id")
        novo_cli = select_id("Cliente", opts_cli_new, key="comp_cli")
        novo_vdd = select_id("Vendedor", opts_vdd_new, key="comp_vdd")
        if st.button("Criar compra em aberto", key="comp_criar"):
            if (novo_cli is None) or (novo_vdd is None):
                st.warning("Selecione cliente e vendedor.")
            else:
                ok, msg = run_write("""
                    INSERT INTO compra (cliente_id, vendedor_id, status, status_pagto)
                    VALUES (%s,%s,'aberto','pendente')
                """, (int(novo_cli), int(novo_vdd)))
                if ok:
                    st.toast("Compra criada! 🧾")
                else:
                    st.error(msg)

    st.divider()

    # 2) Adicionar item
    st.markdown("### 2) Adicionar item à compra")
    if df_abertas.empty:
        st.info("Nenhuma compra em aberto.")
        opts_comp_add = []
    else:
        _, opts_comp_add = pick_id_from(df_abertas, label_col="id", id_col="id")
    comp_id = select_id("Compra (aberta)", opts_comp_add, key="comp_sel_add")

    # apenas produtos ATIVOS para venda
    df_prod2 = run_fetch_df("""
        SELECT id, nome, preco, quantidade
        FROM produtos
        WHERE ativo = TRUE
        ORDER BY nome
    """)
    if df_prod2.empty:
        st.info("Cadastre produtos.")
        opts_prod_add = []
    else:
        _, opts_prod_add = pick_id_from(df_prod2, label_col="nome", id_col="id")
    prod_id = select_id("Produto", opts_prod_add, key="comp_prod_sel")
    qtde = st.number_input("Quantidade", min_value=1, step=1, value=1, key="comp_qtde")

    if st.button("Adicionar item", key="comp_add_item"):
        if (comp_id is None) or (prod_id is None):
            st.warning("Selecione a compra e o produto.")
        else:
            ok, msg = run_write("""
                INSERT INTO item_compra (compra_id, produto_id, qtde, preco_unit)
                SELECT %s, %s, %s, p.preco FROM produtos p WHERE p.id=%s
            """, (int(comp_id), int(prod_id), int(qtde), int(prod_id)))
            if ok:
                st.toast("Item adicionado! ✅")
            else:
                st.error(msg)

    # Itens da compra selecionada
    if comp_id:
        st.markdown("**Itens da compra selecionada**")
        df_itens = run_fetch_df("""
            SELECT ic.id, p.nome, ic.qtde, ic.preco_unit, ic.total_bruto,
                   ic.desconto_aplicado, ic.total_liquido
            FROM item_compra ic
            JOIN produtos p ON p.id = ic.produto_id
            WHERE ic.compra_id = %s
            ORDER BY ic.id
        """, (int(comp_id),))
        st.dataframe(df_itens, use_container_width=True, height=240)

    st.divider()

    # 3) Finalizar
    st.markdown("### 3) Finalizar compra")
    df_abertas2 = run_fetch_df("SELECT id FROM compra WHERE status='aberto' ORDER BY id DESC")
    if df_abertas2.empty or df_forma.empty:
        st.info("Precisa ter compra aberta e formas de pagamento cadastradas.")
    else:
        _, opts_comp_fin = pick_id_from(df_abertas2, label_col="id", id_col="id")
        comp_fin = select_id("Compra (aberta)", opts_comp_fin, key="comp_sel_fin")
        _, opts_fp = pick_id_from(df_forma, label_col="tipo", id_col="id")
        fp_id = select_id("Forma de pagamento", opts_fp, key="comp_fp_sel")
        if st.button("Finalizar (chama stored procedure)", key="comp_finalizar"):
            if (comp_fin is None) or (fp_id is None):
                st.warning("Selecione a compra e a forma de pagamento.")
            else:
                ok, msg = run_write("CALL finalizar_compra(%s, %s)", (int(comp_fin), int(fp_id)))
                if ok:
                    st.toast("Compra finalizada! 🎉")
                else:
                    st.error(msg)

    st.divider()

    # 4) Todas as compras
    st.markdown("### 4) Compras (todas)")
    df_comp_all = run_fetch_df("""
        SELECT id, cliente_id, vendedor_id, data_compra,
               total_bruto, desconto_total, total_liquido,
               status, status_pagto
        FROM compra ORDER BY id DESC
    """)
    st.dataframe(df_comp_all, use_container_width=True, height=320)

# ---------------------- RELATÓRIOS ----------------------
with tabs[4]:
    st.subheader("Relatórios")

    with st.expander("📈 Vendas por vendedor (mês) — via view"):
        # mês padrão = mês atual
        hoje = date.today()
        ref_mes = st.date_input("Mês de referência", value=hoje.replace(day=1), key="rel_ref_mes")
        # a view já traz por mês; filtramos por 'mes'
        df_view = run_fetch_df("""
            SELECT *
            FROM vw_vendas_mensal_vendedor
            WHERE mes = %s
            ORDER BY vendedor_nome
        """, (ref_mes.replace(day=1),))
        st.dataframe(df_view, use_container_width=True, height=320)
