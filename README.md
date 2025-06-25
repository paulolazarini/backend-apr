# 🚀 Documentação da API: Árvore de Pré-Requisitos (APR)

**Versão:** 1.0  
**Data:** 25 de junho de 2025

---

### **🎯 Introdução**

> Esta documentação detalha a API RESTful para o sistema de **Árvore de Pré-Requisitos (APR)**. O objetivo da API é permitir a criação, visualização, atualização e exclusão de árvores de planejamento hierárquicas, associadas a usuários específicos. A estrutura é composta por Árvores (APRs), Objetivos, Obstáculos e Pré-Requisitos, com a capacidade de definir dependências entre eles.

---

### **⚙️ Informações Gerais**

#### **🔗 URL Base**
Todas as URLs documentadas são relativas à seguinte base:

https://backend-apr.vercel.app/api/


#### **🔑 Autenticação**
> A API não requer autenticação por token. As operações são, em sua maioria, públicas, mas a criação de recursos está vinculada a um `user_id` que deve ser fornecido no corpo da requisição para estabelecer a propriedade.

#### **📦 Formato dos Dados**
Todas as requisições e respostas utilizam o formato `application/json`.

#### **🚦 Códigos de Status HTTP**
A API utiliza os seguintes códigos de status para indicar o resultado das operações:

| Código | Descrição |
| :--- | :--- |
| `200 OK` | Requisição bem-sucedida. |
| `201 Created` | Recurso criado com sucesso. |
| `204 No Content`| Recurso deletado com sucesso (sem corpo na resposta). |
| `400 Bad Request`| A requisição contém dados inválidos ou mal formatados. |
| `404 Not Found` | O recurso solicitado não foi encontrado. |
| `500 Internal Server Error` | Ocorreu um erro inesperado no servidor. |

---

### **🌳 Estrutura dos Dados**

A API é organizada em torno da seguinte hierarquia de recursos:

1.  **Usuário (User)**
2.  **Árvore de Pré-Requisitos (APR)**
    * **Objetivo(s)**
        * **Obstáculo(s)**
            * **Pré-Requisito(s)**
                * **Dependências** (relação entre dois Pré-Requisitos)

---

### **🔌 Endpoints da API**

#### **1. Árvore de Pré-Requisitos (APR)**
> Recurso principal que representa uma árvore de planejamento completa.

##### **1.1. Listar todas as APRs**
* **Endpoint:** `GET /apr/`
* **Descrição:** Retorna uma lista de todas as árvores de pré-requisitos disponíveis. Para otimização, os nós aninhados não são incluídos nesta listagem.
* **Resposta de Sucesso (200 OK):** Uma lista de objetos APR.

##### **1.2. Detalhes de uma APR (Recuperar a Árvore Completa)**
* **Endpoint:** `GET /test-view-tree/{id}/`
* **Descrição:** Retorna um único objeto APR com toda a sua estrutura aninhada: objetivos, obstáculos e pré-requisitos. Este é o endpoint recomendado para renderizar a visualização completa de uma árvore.
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "id": 13,
        "nome_apr": "Aprendizado de Python",
        "description": "Árvore para aprender Python do zero",
        "user": { "id": 2, "username": "joao_silva" },
        "objetivos": [
            {
                "id": 2,
                "nome_objetivo": "Python Básico",
                "obstaculos": [
                    {
                        "id": 1,
                        "nome_obstaculo": "Sintaxe Python",
                        "prerequisitos": [
                            {
                                "id": 1,
                                "nome_requisito": "Variáveis",
                                "priority": 1,
                                "priority_display": "Baixa"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    ```

##### **1.3. Criar uma nova APR**
* **Endpoint:** `POST /apr/`
* **Corpo da Requisição:**
    ```json
    {
        "nome_apr": "String (Obrigatório)",
        "description": "String (Opcional)",
        "user_id": "Integer (ID do usuário, Obrigatório)"
    }
    ```
* **Resposta de Sucesso (201 Created):** O objeto da APR recém-criada.

##### **1.4. Atualizar uma APR**
* **Endpoint:** `PUT /apr/{id}/`
* **Corpo da Requisição:** Os mesmos campos da criação, exceto `user_id`.

##### **1.5. Deletar uma APR**
* **Endpoint:** `DELETE /apr/{id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **2. Objetivos**

##### **2.1. Criar um Objetivo**
* **Endpoint:** `POST /apr/{apr_id}/objetivos/`
* **Corpo da Requisição:**
    ```json
    {
        "nome_objetivo": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```

##### **2.2. Atualizar um Objetivo**
* **Endpoint:** `PUT /apr/{apr_id}/objetivos/{objetivo_id}/`

##### **2.3. Deletar um Objetivo**
* **Endpoint:** `DELETE /apr/{apr_id}/objetivos/{objetivo_id}/`

---

#### **3. Obstáculos**

##### **3.1. Criar um Obstáculo**
* **Endpoint:** `POST /objetivos/{objetivo_id}/obstaculos/`
* **Corpo da Requisição:**
    ```json
    {
        "nome_obstaculo": "String (Obrigatório)",
        "description": "String (Opcional)"
    }
    ```

##### **3.2. Atualizar um Obstáculo**
* **Endpoint:** `PUT /objetivos/{objetivo_id}/obstaculos/{obstaculo_id}/`

##### **3.3. Deletar um Obstáculo**
* **Endpoint:** `DELETE /objetivos/{objetivo_id}/obstaculos/{obstaculo_id}/`

---

#### **4. Pré-Requisitos**

##### **4.1. Criar um Pré-Requisito**
* **Endpoint:** `POST /obstaculos/{obstaculo_id}/prerequisitos/`
* **Corpo da Requisição:**
    ```json
    {
        "nome_requisito": "String (Obrigatório)",
        "description": "String (Opcional)",
        "priority": "Integer (Obrigatório)" // 1=Baixa, 2=Média, 3=Alta
    }
    ```

##### **4.2. Atualizar um Pré-Requisito**
* **Endpoint:** `PUT /obstaculos/{obstaculo_id}/prerequisitos/{prerequisito_id}/`

##### **4.3. Deletar um Pré-Requisito**
* **Endpoint:** `DELETE /obstaculos/{obstaculo_id}/prerequisitos/{prerequisito_id}/`

---

#### **5. Dependências**

##### **5.1. Criar uma Dependência**
* **Endpoint:** `POST /dependencias/`
* **Descrição:** Cria uma relação onde um pré-requisito (`requisito_alvo`) depende de outro (`requisito_origem`).
* **Corpo da Requisição:**
    ```json
    {
        "requisito_origem": "Integer (ID do pré-requisito)",
        "requisito_alvo": "Integer (ID do pré-requisito)"
    }
    ```

##### **5.2. Deletar uma Dependência**
* **Endpoint:** `DELETE /dependencias/{id}/`

---

### **💡 Guia Rápido para o Desenvolvedor Front-End**

* **Fluxo de Trabalho:**
    1.  **Dashboard:** Use `GET /apr/` para listar todas as árvores disponíveis e permitir que o usuário selecione uma.
    2.  **Visualização:** Use `GET /test-view-tree/{id}/` para buscar a estrutura completa da APR selecionada e renderizá-la na interface.
    3.  **Interação:** Use os endpoints de `POST`, `PUT` e `DELETE` para criar, editar e excluir nós da árvore nos seus respectivos níveis (APR, Objetivo, Obstáculo, etc.). O ID do nó pai é passado na URL, simplificando as requisições.

* **Mapeamento de Dados para a UI:**
    * **Prioridades:** Use o campo `priority_display` para exibir o texto ("Alta") e o campo `priority` (ex: 3) para lógica interna ou estilos CSS.
    * **Estrutura de Criação:** Ao criar um item aninhado (ex: um Objetivo), o ID do pai (APR) já está na URL (`/apr/{apr_id}/objetivos/`), o que significa que o `arvore_id` não precisa ser enviado no corpo da requisição.
