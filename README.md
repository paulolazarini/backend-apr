# Documentação da API: Árvore de Pré-Requisitos (APR)

**Versão:** 1.0
**Data:** 13 de junho de 2025

### Introdução

Esta documentação detalha a API RESTful para o sistema de Árvore de Pré-Requisitos (APR). O objetivo da API é permitir a criação, visualização, atualização e exclusão de árvores de planejamento hierárquicas, compostas por Objetivos, Obstáculos e Pré-Requisitos.

### Informações Gerais

#### URL Base
Todas as URLs documentadas são relativas à seguinte base:
`https://sua-api.com/api/`

#### Autenticação
A API utiliza autenticação por Token. Todas as requisições (exceto o login para obter o token) devem incluir o cabeçalho `Authorization`.

**Exemplo de Cabeçalho:**

#### Formato dos Dados
Todas as requisições e respostas utilizam o formato `application/json`.

#### Códigos de Status HTTP
A API utiliza os seguintes códigos de status para indicar o resultado das operações:
-   `200 OK`: Requisição bem-sucedida.
-   `201 Created`: Recurso criado com sucesso.
-   `204 No Content`: Recurso deletado com sucesso (sem corpo na resposta).
-   `400 Bad Request`: A requisição contém dados inválidos ou mal formatados.
-   `401 Unauthorized`: Autenticação falhou ou não foi fornecida.
-   `403 Forbidden`: O usuário autenticado não tem permissão para realizar a ação.
-   `404 Not Found`: O recurso solicitado não foi encontrado.

---

### Estrutura dos Dados

A API é organizada em torno da seguinte hierarquia de recursos:

-   **Árvore de Pré-Requisitos (APR)**
    -   **Objetivo(s)**
        -   **Obstáculo(s)**
            -   **Pré-Requisito(s)**
-   **Dependências** (relação entre dois Pré-Requisitos)

---

## Endpoints da API

### 1. Árvore de Pré-Requisitos (APR)

Recurso principal que representa uma árvore de planejamento completa.

#### 1.1. Listar todas as APRs do usuário
-   **Endpoint:** `GET /arvores/`
-   **Descrição:** Retorna uma lista de todas as árvores de pré-requisitos que pertencem ao usuário autenticado.
-   **Resposta de Sucesso (200 OK):** Uma lista de objetos APR. A estrutura de cada objeto é idêntica à do endpoint de "Detalhes da APR" (1.2).

#### 1.2. Detalhes de uma APR (Recuperar a Árvore Completa)
-   **Endpoint:** `GET /arvores/{id}/`
-   **Descrição:** Retorna um único objeto APR com toda a sua estrutura aninhada.
-   **Resposta de Sucesso (200 OK):**
    ```json
    {
        "id": 1,
        "nome_apr": "Lançamento do Projeto Phoenix",
        "description": "Todos os passos para o lançamento.",
        "user": { "id": 1, "username": "paulo_lazarini" },
        "objetivos": [
            {
                "id": 1,
                "nome_objetivo": "Finalizar o Desenvolvimento",
                "obstaculos": [
                    {
                        "id": 1,
                        "nome_obstaculo": "Corrigir Bugs Críticos",
                        "pre_requisitos": [
                            {
                                "id": 1,
                                "nome_requisito": "Testar o fluxo de login",
                                "priority": 3,
                                "priority_display": "Alta"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

#### 1.3. Criar uma nova APR
-   **Endpoint:** `POST /arvores/`
-   **Corpo da Requisição:**
    ```json
    {
        "nome_apr": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```
-   **Resposta de Sucesso (201 Created):** O objeto da APR recém-criada.

#### 1.4. Atualizar uma APR
-   **Endpoint:** `PUT /arvores/{id}/` ou `PATCH /arvores/{id}/`
-   **Corpo da Requisição:**
    ```json
    {
        "nome_apr": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```

#### 1.5. Deletar uma APR
-   **Endpoint:** `DELETE /arvores/{id}/`
-   **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

### 2. Objetivos

#### 2.1. Criar um Objetivo
-   **Endpoint:** `POST /arvores/{arvore_id}/objetivos/`
-   **Corpo da Requisição:**
    ```json
    {
        "nome_objetivo": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```

#### 2.2. Atualizar um Objetivo
-   **Endpoint:** `PUT /objetivos/{id}/`
-   **Corpo da Requisição:** `{ "nome_objetivo": "...", "description": "..." }`

#### 2.3. Deletar um Objetivo
-   **Endpoint:** `DELETE /objetivos/{id}/`

---

### 3. Obstáculos

#### 3.1. Criar um Obstáculo
-   **Endpoint:** `POST /objetivos/{objetivo_id}/obstaculos/`
-   **Corpo da Requisição:**
    ```json
    {
        "nome_obstaculo": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```

#### 3.2. Atualizar um Obstáculo
-   **Endpoint:** `PUT /obstaculos/{id}/`
-   **Corpo da Requisição:** `{ "nome_obstaculo": "...", "description": "..." }`

#### 3.3. Deletar um Obstáculo
-   **Endpoint:** `DELETE /obstaculos/{id}/`

---

### 4. Pré-Requisitos

#### 4.1. Criar um Pré-Requisito
-   **Endpoint:** `POST /obstaculos/{obstaculo_id}/pre-requisitos/`
-   **Corpo da Requisição:**
    ```json
    {
        "nome_requisito": "String (Obrigatório)",
        "description": "String (Opcional)",
        "priority": "Integer (Obrigatório)" // 1=Baixa, 2=Média, 3=Alta
    }
    ```

#### 4.2. Atualizar um Pré-Requisito
-   **Endpoint:** `PUT /pre-requisitos/{id}/`
-   **Corpo da Requisição:** `{ "nome_requisito": "...", "description": "...", "priority": 2 }`

#### 4.3. Deletar um Pré-Requisito
-   **Endpoint:** `DELETE /pre-requisitos/{id}/`

### 5. Dependências

#### 5.1. Listar todas as Dependências
-   **Endpoint:** `GET /dependencias/`

#### 5.2. Criar uma Dependência
-   **Endpoint:** `POST /dependencias/`
-   **Corpo da Requisição:**
    ```json
    {
        "requisito_origem": "Integer (ID do pré-requisito)",
        "requisito_alvo": "Integer (ID do pré-requisito)"
    }
    ```

#### 5.3. Deletar uma Dependência
-   **Endpoint:** `DELETE /dependencias/{id}/`

---

### Guia Rápido para o Desenvolvedor Front-End

1.  **Fluxo de Trabalho:**
    a. **Login:** Obtenha o token de autenticação.
    b. **Dashboard:** Use `GET /arvores/` para listar as árvores do usuário.
    c. **Visualização:** Use `GET /arvores/{id}/` para buscar e renderizar a árvore completa.
    d. **Interação:** Use os endpoints de `POST`, `PUT` e `DELETE` para criar, editar e excluir nós da árvore nos seus respectivos níveis.

2.  **Mapeamento de Dados para a UI:**
    -   **Prioridades:** Use `priority_display` para o texto ("Alta") e `priority` (3) para lógica ou estilos CSS.
    -   **Formulários:** Lembre-se que ao criar um item aninhado, o ID do pai vem da URL, simplificando o corpo da requisição.
