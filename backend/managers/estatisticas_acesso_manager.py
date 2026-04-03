from collections import defaultdict
from datetime import datetime

from repositories.repository_factory import repository_factory


class EstatisticasAcessoManager:
    """Manager para consolidar estatisticas de acesso dos usuarios."""

    def __init__(self):
        self.acesso_usuario_repository = repository_factory.get_acesso_usuario_repository()

    def listar_acessos_brutos(self):
        """
        Lista os registros brutos de acesso.

        :return: lista de objetos AcessoUsuario
        """
        return self.acesso_usuario_repository.listar()

    def obter_estatisticas_acesso(self):
        """
        Consolida estatisticas de acesso a partir do historico de logins.

        :return: dict com agregacoes de acessos
        """
        acessos = self.listar_acessos_brutos()
        return self.consolidar_estatisticas(acessos)

    def consolidar_estatisticas(self, acessos):
        """
        Consolida estatisticas a partir de uma lista de acessos.

        :param acessos: lista de objetos AcessoUsuario
        :return: dict com agregacoes de acessos
        """

        usuarios_index = {}
        acessos_por_dia = defaultdict(int)
        acessos_por_semana = defaultdict(int)
        acessos_por_mes = defaultdict(int)
        acessos_por_tipo_usuario = defaultdict(int)

        for acesso in acessos:
            data_hora_acesso = self._normalizar_data_hora(acesso.data_hora_acesso)
            usuario_key = self._criar_chave_usuario(acesso.usuario_id, acesso.tipo_usuario)

            if usuario_key not in usuarios_index:
                usuarios_index[usuario_key] = {
                    'usuario_id': acesso.usuario_id,
                    'tipo_usuario': acesso.tipo_usuario,
                    'email': acesso.email,
                    'quantidade_acessos': 0,
                    'ultimo_acesso': None
                }

            usuario_stats = usuarios_index[usuario_key]
            usuario_stats['quantidade_acessos'] += 1

            if (
                usuario_stats['ultimo_acesso'] is None or
                data_hora_acesso > datetime.fromisoformat(usuario_stats['ultimo_acesso'])
            ):
                usuario_stats['ultimo_acesso'] = data_hora_acesso.isoformat()

            acessos_por_tipo_usuario[acesso.tipo_usuario] += 1
            acessos_por_dia[data_hora_acesso.strftime('%Y-%m-%d')] += 1
            acessos_por_mes[data_hora_acesso.strftime('%Y-%m')] += 1

            ano_iso, semana_iso, _ = data_hora_acesso.isocalendar()
            chave_semana = f'{ano_iso}-W{semana_iso:02d}'
            acessos_por_semana[chave_semana] += 1

        usuarios_que_acessaram = list(usuarios_index.values())
        usuarios_que_acessaram.sort(
            key=lambda usuario: usuario['ultimo_acesso'] or '',
            reverse=True
        )

        ultimo_acesso_por_usuario = [
            {
                'usuario_id': usuario['usuario_id'],
                'tipo_usuario': usuario['tipo_usuario'],
                'email': usuario['email'],
                'ultimo_acesso': usuario['ultimo_acesso']
            }
            for usuario in usuarios_que_acessaram
        ]

        return {
            'total_logins': len(acessos),
            'usuarios_que_acessaram': usuarios_que_acessaram,
            'ultimo_acesso_por_usuario': ultimo_acesso_por_usuario,
            'acessos_por_periodo': {
                'dia': dict(sorted(acessos_por_dia.items())),
                'semana': dict(sorted(acessos_por_semana.items())),
                'mes': dict(sorted(acessos_por_mes.items()))
            },
            'acessos_por_tipo_usuario': dict(sorted(acessos_por_tipo_usuario.items()))
        }

    def _normalizar_data_hora(self, valor):
        """Normaliza valores de data/hora vindos do repositorio."""
        if isinstance(valor, datetime):
            return valor

        if isinstance(valor, str):
            return datetime.fromisoformat(valor)

        raise TypeError("Formato de data_hora_acesso invalido")

    def _criar_chave_usuario(self, usuario_id, tipo_usuario):
        """Cria uma chave unica para agregar acessos por usuario e tipo."""
        return f'{tipo_usuario}:{usuario_id}'


estatisticas_acesso_manager = EstatisticasAcessoManager()
