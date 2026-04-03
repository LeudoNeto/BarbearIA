from datetime import datetime
from html import escape

from services.relatorio_acessos_template import RelatorioAcessosTemplate


class RelatorioAcessosHTML(RelatorioAcessosTemplate):
    """Relatorio concreto de acessos em HTML."""

    def montar_cabecalho(self, estatisticas):
        data_geracao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"""
<header>
  <h1>Relatório de Acessos dos Usuários</h1>
  <p>Gerado em: {escape(data_geracao)}</p>
  <p>Total de logins: {estatisticas['total_logins']}</p>
</header>
""".strip()

    def montar_corpo(self, estatisticas):
        return "\n".join([
            self._montar_secao_usuarios(estatisticas['usuarios_que_acessaram']),
            self._montar_secao_periodo(estatisticas['acessos_por_periodo']),
            self._montar_secao_tipo(estatisticas['acessos_por_tipo_usuario'])
        ])

    def montar_rodape(self, estatisticas):
        total_usuarios = len(estatisticas['usuarios_que_acessaram'])
        return f"""
<footer>
  <p>Total de usuarios distintos com acesso registrado: {total_usuarios}</p>
</footer>
""".strip()

    def gerar_saida_final(self, cabecalho, corpo, rodape, estatisticas):
        return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Relatorio de Acessos</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
    h1, h2 {{ color: #111; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #f3f3f3; }}
    section {{ margin-bottom: 24px; }}
    footer {{ margin-top: 32px; font-size: 0.95rem; color: #555; }}
  </style>
</head>
<body>
  {cabecalho}
  {corpo}
  {rodape}
</body>
</html>"""

    def _montar_secao_usuarios(self, usuarios):
        linhas = []
        for usuario in usuarios:
            linhas.append(
                "<tr>"
                f"<td>{usuario['usuario_id']}</td>"
                f"<td>{escape(usuario['tipo_usuario'])}</td>"
                f"<td>{escape(usuario['email'])}</td>"
                f"<td>{usuario['quantidade_acessos']}</td>"
                f"<td>{escape(usuario['ultimo_acesso'] or '-')}</td>"
                "</tr>"
            )

        corpo_tabela = "\n".join(linhas) or (
            '<tr><td colspan="5">Nenhum acesso registrado.</td></tr>'
        )

        return f"""
<section>
  <h2>Usuarios que acessaram</h2>
  <table>
    <thead>
      <tr>
        <th>ID</th>
        <th>Tipo</th>
        <th>Email</th>
        <th>Quantidade de acessos</th>
        <th>Ultimo acesso</th>
      </tr>
    </thead>
    <tbody>
      {corpo_tabela}
    </tbody>
  </table>
</section>
""".strip()

    def _montar_secao_periodo(self, acessos_por_periodo):
        secoes = []
        for nome_periodo, valores in acessos_por_periodo.items():
            itens = []
            for chave, total in valores.items():
                itens.append(f"<li>{escape(chave)}: {total}</li>")

            conteudo = "\n".join(itens) or "<li>Nenhum acesso registrado.</li>"
            secoes.append(
                f"""
<h3>Por {escape(nome_periodo)}</h3>
<ul>
  {conteudo}
</ul>
""".strip()
            )

        return f"""
<section>
  <h2>Acessos por periodo</h2>
  {' '.join(secoes)}
</section>
""".strip()

    def _montar_secao_tipo(self, acessos_por_tipo_usuario):
        itens = []
        for tipo_usuario, total in acessos_por_tipo_usuario.items():
            itens.append(f"<li>{escape(tipo_usuario)}: {total}</li>")

        conteudo = "\n".join(itens) or "<li>Nenhum acesso registrado.</li>"
        return f"""
<section>
  <h2>Acessos por tipo de usuario</h2>
  <ul>
    {conteudo}
  </ul>
</section>
""".strip()
