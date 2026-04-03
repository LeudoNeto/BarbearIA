from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from services.relatorio_acessos_template import RelatorioAcessosTemplate


class RelatorioAcessosPDF(RelatorioAcessosTemplate):
    """Relatorio concreto de acessos em PDF."""

    def montar_cabecalho(self, estatisticas):
        return {
            'titulo': 'Relatorio de Acessos dos Usuarios',
            'gerado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_logins': estatisticas['total_logins']
        }

    def montar_corpo(self, estatisticas):
        return {
            'usuarios': estatisticas['usuarios_que_acessaram'],
            'periodos': estatisticas['acessos_por_periodo'],
            'tipos': estatisticas['acessos_por_tipo_usuario']
        }

    def montar_rodape(self, estatisticas):
        return {
            'total_usuarios_distintos': len(estatisticas['usuarios_que_acessaram'])
        }

    def gerar_saida_final(self, cabecalho, corpo, rodape, estatisticas):
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm
        )
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(cabecalho['titulo'], styles['Title']))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(f"Gerado em: {cabecalho['gerado_em']}", styles['Normal']))
        story.append(Paragraph(f"Total de logins: {cabecalho['total_logins']}", styles['Normal']))
        story.append(Spacer(1, 0.5 * cm))

        story.append(Paragraph("Usuarios que acessaram", styles['Heading2']))
        story.append(self._montar_tabela_usuarios(corpo['usuarios']))
        story.append(Spacer(1, 0.5 * cm))

        story.append(Paragraph("Acessos por periodo", styles['Heading2']))
        for nome_periodo, valores in corpo['periodos'].items():
            story.append(Paragraph(f"Por {nome_periodo}", styles['Heading3']))
            story.append(self._montar_tabela_periodo(valores))
            story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph("Acessos por tipo de usuario", styles['Heading2']))
        story.append(self._montar_tabela_tipo(corpo['tipos']))
        story.append(Spacer(1, 0.5 * cm))

        story.append(
            Paragraph(
                f"Total de usuarios distintos com acesso registrado: {rodape['total_usuarios_distintos']}",
                styles['Italic']
            )
        )

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def _montar_tabela_usuarios(self, usuarios):
        dados = [[
            'ID',
            'Tipo',
            'Email',
            'Qtd. acessos',
            'Ultimo acesso'
        ]]

        if usuarios:
            for usuario in usuarios:
                dados.append([
                    str(usuario['usuario_id']),
                    usuario['tipo_usuario'],
                    usuario['email'],
                    str(usuario['quantidade_acessos']),
                    usuario['ultimo_acesso'] or '-'
                ])
        else:
            dados.append(['-', '-', 'Nenhum acesso registrado.', '-', '-'])

        return self._criar_tabela(dados, [1.2 * cm, 2.8 * cm, 6.8 * cm, 2.4 * cm, 4.8 * cm])

    def _montar_tabela_periodo(self, valores):
        dados = [['Periodo', 'Quantidade']]

        if valores:
            for chave, total in valores.items():
                dados.append([chave, str(total)])
        else:
            dados.append(['Nenhum acesso registrado.', '-'])

        return self._criar_tabela(dados, [8 * cm, 4 * cm])

    def _montar_tabela_tipo(self, valores):
        dados = [['Tipo de usuario', 'Quantidade']]

        if valores:
            for tipo_usuario, total in valores.items():
                dados.append([tipo_usuario, str(total)])
        else:
            dados.append(['Nenhum acesso registrado.', '-'])

        return self._criar_tabela(dados, [8 * cm, 4 * cm])

    def _criar_tabela(self, dados, col_widths):
        tabela = Table(dados, colWidths=col_widths, repeatRows=1)
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eaeaea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdbdbd')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f8f8')]),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        return tabela
