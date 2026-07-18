from crewai.tools import tool
import httpx

BASE_URL = "http://127.0.0.1:8000"

@tool("Listar Tasks")
def listar_tasks(query: str) -> str:
    """Lista todas as tasks disponíveis na API. Use quando o usuário quiser ver suas tasks."""
    try:
        # Nota: Usando prefixo /v1/tasks/ conforme configurado na API TaskManager
        resposta = httpx.get(f"{BASE_URL}/v1/tasks/?limit=100")
        resposta.raise_for_status()
        tasks = resposta.json()
        if not tasks:
            return "Nenhuma task encontrada."
        # Filtra chaves irrelevantes para economizar tokens na LLM
        tasks_simplificadas = [
            {"id": t.get("id"), "title": t.get("title"), "status": t.get("status")}
            for t in tasks
        ]
        return str(tasks_simplificadas)
    except httpx.ConnectError:
        return "Erro: Não foi possível conectar ao servidor. Por favor, verifique se a API do TaskManager está ativa."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return "Erro: O endpoint de listagem de tarefas não foi encontrado no servidor (Erro 404)."
        return f"Erro na API (Status {e.response.status_code}): Não foi possível obter a lista de tarefas no momento."
    except Exception as e:
        return "Não foi possível listar as tarefas devido a um erro inesperado na API."


@tool("Criar Task")
def criar_task(titulo: str) -> str:
    """Cria uma nova task na API. Requer o título da task."""
    try:
        resposta = httpx.post(
            f"{BASE_URL}/v1/tasks/",
            json={"title": titulo} # A API espera 'title' em vez de 'titulo'
        )
        resposta.raise_for_status()
        task = resposta.json()
        return f"Task criada com sucesso: ID {task.get('id')} - {task.get('title')}"
    except httpx.ConnectError:
        return "Erro: Não foi possível conectar ao servidor. Por favor, verifique se a API do TaskManager está ativa."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return "Erro: O servidor retornou que o recurso de criação não foi encontrado (Erro 404)."
        if e.response.status_code == 422:
            return "Erro: Os dados enviados para criar a tarefa são inválidos."
        return f"Erro na API (Status {e.response.status_code}): Não foi possível criar a tarefa."
    except Exception as e:
        return "Não foi possível criar a tarefa devido a um erro inesperado na API."


@tool("Deletar Task")
def deletar_task(task_id: str) -> str:
    """Deleta uma task pelo ID. Requer o ID numérico da task."""
    try:
        resposta = httpx.delete(f"{BASE_URL}/v1/tasks/{task_id}")
        resposta.raise_for_status()
        return f"Task {task_id} deletada com sucesso."
    except httpx.ConnectError:
        return "Erro: Não foi possível conectar ao servidor. Por favor, verifique se a API do TaskManager está ativa."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Erro: A tarefa com ID '{task_id}' não foi encontrada (Erro 404)."
        return f"Erro na API (Status {e.response.status_code}): Não foi possível deletar a tarefa."
    except Exception as e:
        return "Não foi possível deletar a tarefa devido a um erro inesperado na API."


@tool("Atualizar Task")
def atualizar_task(task_id: str, titulo: str = None, status: str = None) -> str:
    """Atualiza uma task pelo ID. Pode atualizar título e/ou status.
    Status válidos: pending, in_progress, done"""
    try:
        body = {}
        if titulo:
            body["title"] = titulo # A API espera 'title'
        if status:
            body["status"] = status

        resposta = httpx.put(
            f"{BASE_URL}/v1/tasks/{task_id}",
            json=body
        )
        resposta.raise_for_status()
        task = resposta.json()
        return f"Task atualizada: ID {task.get('id')} - {task.get('title')} - {task.get('status')}"
    except httpx.ConnectError:
        return "Erro: Não foi possível conectar ao servidor. Por favor, verifique se a API do TaskManager está ativa."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return f"Erro: A tarefa com ID '{task_id}' não foi encontrada (Erro 404)."
        if e.response.status_code == 422:
            return "Erro: Os dados enviados para atualizar a tarefa são inválidos."
        return f"Erro na API (Status {e.response.status_code}): Não foi possível atualizar a tarefa."
    except Exception as e:
        return "Não foi possível atualizar a tarefa devido a um erro inesperado na API."


@tool("Buscar Task por Título")
def buscar_task_por_titulo(titulo: str) -> str:
    """Busca o ID de uma task pelo título. Use quando o usuário mencionar o nome da task
    mas não o ID, e você precisar do ID para deletar ou atualizar."""
    try:
        resposta = httpx.get(f"{BASE_URL}/v1/tasks/?limit=100")
        resposta.raise_for_status()
        tasks = resposta.json()
        titulo_lower = titulo.lower()
        # A API retorna objetos com chave 'title'
        matches = [t for t in tasks if titulo_lower in t.get("title", "").lower()]
        if not matches:
            return f"Nenhuma task encontrada com título contendo '{titulo}'."
        # Filtra chaves irrelevantes para economizar tokens
        matches_simplificados = [
            {"id": t.get("id"), "title": t.get("title"), "status": t.get("status")}
            for t in matches
        ]
        return str(matches_simplificados)
    except httpx.ConnectError:
        return "Erro: Não foi possível conectar ao servidor. Por favor, verifique se a API do TaskManager está ativa."
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return "Erro: O servidor retornou que o recurso de busca não foi encontrado (Erro 404)."
        return f"Erro na API (Status {e.response.status_code}): Não foi possível buscar a tarefa."
    except Exception as e:
        return "Não foi possível buscar a tarefa devido a um erro inesperado na API."
