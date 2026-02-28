from fastapi import FastAPI
from controllers.auth_controller import auth_controller
from controllers.cliente_controller import cliente_controller
from controllers.funcionario_controller import funcionario_controller
from controllers.empresa_controller import empresa_controller
from controllers.horario_funcionamento_controller import horario_funcionamento_controller
from controllers.agendamento_controller import agendamento_controller


# Inicializa a aplicação FastAPI
app = FastAPI(title='BarbearIA API', version='1.0.0')

# Registra as rotas
app.include_router(auth_controller.router)
app.include_router(cliente_controller.router)
app.include_router(funcionario_controller.router)
app.include_router(empresa_controller.router)
app.include_router(horario_funcionamento_controller.router)
app.include_router(agendamento_controller.router)


@app.get('/')
async def root():
    """Endpoint raiz da API"""
    return {
        'message': 'BarbearIA API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/auth',
            'clientes': '/clientes',
            'funcionarios': '/funcionarios',
            'empresa': '/empresa',
            'horarios_funcionamento': '/horarios-funcionamento',
            'agendamentos': '/agendamentos'
        }
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
