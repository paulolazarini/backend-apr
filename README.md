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

#### **0. Usuários (Users)**

##### **0.1. Listar Usuários**
* **Endpoint:** `GET /users/`
* **Descrição:** Retorna uma lista de todos os usuários cadastrados.
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 1,
        "username": "joao_silva",
        "first_name": "João",
        "last_name": "Silva",
        "email": "joao.silva@email.com"
    }
]
```

##### **0.2. Criar Usuário**
* **Endpoint:** `POST /users/create/`
* **Corpo da Requisição:**
```json
{
    "username": "String (Obrigatório, não pode ser vazio)",
    "password": "String (Obrigatório, não pode ser vazio)",
    "first_name": "String (Opcional, se enviado não pode ser vazio)",
    "last_name": "String (Opcional, se enviado não pode ser vazio)",
    "email": "String (Opcional, se enviado não pode ser vazio e deve ser e-mail válido)"
}
```
* **Observação:** Se não quiser preencher os campos opcionais, basta omiti-los do JSON.
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 2,
    "username": "novo_usuario",
    "first_name": "Nome",
    "last_name": "Sobrenome",
    "email": "email@exemplo.com"
}
```

##### **0.3. Ver Usuário Específico**
* **Endpoint:** `GET /users/{id}/`
* **Resposta de Sucesso (200 OK):**
```json
{
    "id": 1,
    "username": "joao_silva",
    "first_name": "João",
    "last_name": "Silva",
    "email": "joao.silva@email.com"
}
```

##### **0.4. Atualizar Usuário**
* **Endpoint:** `PUT /users/{id}/`
* **Corpo da Requisição:**
```json
{
    "username": "String (Opcional, não pode ser vazio)",
    "password": "String (Opcional, se enviado será atualizada a senha)",
    "first_name": "String (Opcional, se enviado não pode ser vazio)",
    "last_name": "String (Opcional, se enviado não pode ser vazio)",
    "email": "String (Opcional, se enviado não pode ser vazio e deve ser e-mail válido)"
}
```

##### **0.5. Deletar Usuário**
* **Endpoint:** `DELETE /users/{id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **1. Árvore de Pré-Requisitos (APR)**

##### **1.1. Listar todas as APRs**
* **Endpoint:** `GET /apr/`
* **Descrição:** Retorna uma lista de todas as árvores de pré-requisitos disponíveis.
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 13,
        "nome_apr": "Aprendizado de Python",
        "description": "Árvore para aprender Python do zero",
        "user": {
            "id": 2,
            "username": "joao_silva",
            "first_name": "João",
            "last_name": "Silva"
        },
        "objetivos": []
    }
]
```

##### **1.2. Ver ARP Específica**
* **Endpoint:** `GET /apr/{id}/`
* **Resposta de Sucesso (200 OK):**
```json
{
    "id": 13,
    "nome_apr": "Aprendizado de Python",
    "description": "Árvore para aprender Python do zero",
    "user": {
        "id": 2,
        "username": "joao_silva",
        "first_name": "João",
        "last_name": "Silva"
    },
    "objetivos": []
}
```

##### **1.3. Criar uma nova APR**
* **Endpoint:** `POST /apr/`
* **Corpo da Requisição:**
```json
{
    "nome_apr": "String (Obrigatório, não pode ser vazio)",
    "description": "String (Opcional)",
    "user_id": "Integer (ID do usuário, Obrigatório)"
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 14,
    "nome_apr": "Nova Árvore",
    "description": "Descrição da árvore",
    "user": {
        "id": 2,
        "username": "joao_silva",
        "first_name": "João",
        "last_name": "Silva"
    },
    "objetivos": []
}
```

##### **1.4. Atualizar uma APR**
* **Endpoint:** `PUT /apr/{id}/`
* **Corpo da Requisição:**
```json
{
    "nome_apr": "String (Opcional, não pode ser vazio)",
    "description": "String (Opcional)"
}
```

##### **1.5. Deletar uma APR**
* **Endpoint:** `DELETE /apr/{id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **2. Objetivos**

##### **2.1. Listar Objetivos de uma ARP**
* **Endpoint:** `GET /apr/{apr_id}/objetivos/`
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 2,
        "nome_objetivo": "Python Básico",
        "description": "Aprender fundamentos",
        "obstaculos": []
    }
]
```

##### **2.2. Criar um Objetivo**
* **Endpoint:** `POST /apr/{apr_id}/objetivos/`
* **Corpo da Requisição:**
```json
{
    "nome_objetivo": "String (Obrigatório, não pode ser vazio)",
    "description": "String (Opcional)"
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 3,
    "nome_objetivo": "Novo Objetivo",
    "description": "Descrição do objetivo",
    "obstaculos": []
}
```

##### **2.3. Ver Objetivo Específico**
* **Endpoint:** `GET /apr/{apr_id}/objetivos/{objetivo_id}/`
* **Resposta de Sucesso (200 OK):**
```json
{
    "id": 2,
    "nome_objetivo": "Python Básico",
    "description": "Aprender fundamentos",
    "obstaculos": []
}
```

##### **2.4. Atualizar um Objetivo**
* **Endpoint:** `PUT /apr/{apr_id}/objetivos/{objetivo_id}/`
* **Corpo da Requisição:**
```json
{
    "nome_objetivo": "String (Opcional, não pode ser vazio)",
    "description": "String (Opcional)"
}
```

##### **2.5. Deletar um Objetivo**
* **Endpoint:** `DELETE /apr/{apr_id}/objetivos/{objetivo_id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **3. Obstáculos**

##### **3.1. Listar Obstáculos de um Objetivo**
* **Endpoint:** `GET /objetivos/{objetivo_id}/obstaculos/`
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 1,
        "nome_obstaculo": "Sintaxe Python",
        "description": "Entender sintaxe básica",
        "pre_requisitos": []
    }
]
```

##### **3.2. Criar um Obstáculo**
* **Endpoint:** `POST /objetivos/{objetivo_id}/obstaculos/`
* **Corpo da Requisição:**
```json
{
    "nome_obstaculo": "String (Obrigatório, não pode ser vazio)",
    "description": "String (Opcional)"
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 2,
    "nome_obstaculo": "Novo Obstáculo",
    "description": "Descrição do obstáculo",
    "pre_requisitos": []
}
```

##### **3.3. Ver Obstáculo Específico**
* **Endpoint:** `GET /objetivos/{objetivo_id}/obstaculos/{obstaculo_id}/`
* **Resposta de Sucesso (200 OK):**
```json
{
    "id": 1,
    "nome_obstaculo": "Sintaxe Python",
    "description": "Entender sintaxe básica",
    "pre_requisitos": []
}
```

##### **3.4. Atualizar um Obstáculo**
* **Endpoint:** `PUT /objetivos/{objetivo_id}/obstaculos/{obstaculo_id}/`
* **Corpo da Requisição:**
```json
{
    "nome_obstaculo": "String (Opcional, não pode ser vazio)",
    "description": "String (Opcional)"
}
```

##### **3.5. Deletar um Obstáculo**
* **Endpoint:** `DELETE /objetivos/{objetivo_id}/obstaculos/{obstaculo_id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **4. Pré-Requisitos**

##### **4.1. Listar Pré-requisitos de um Obstáculo**
* **Endpoint:** `GET /obstaculos/{obstaculo_id}/prerequisitos/`
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 1,
        "nome_requisito": "Variáveis",
        "description": "Aprender variáveis",
        "priority": 1,
        "priority_display": "Baixa"
    }
]
```

##### **4.2. Criar um Pré-Requisito**
* **Endpoint:** `POST /obstaculos/{obstaculo_id}/prerequisitos/`
* **Corpo da Requisição:**
```json
{
    "nome_requisito": "String (Obrigatório, não pode ser vazio)",
    "description": "String (Opcional)",
    "priority": "Integer (Opcional, default: 2=Média)" // 1=Baixa, 2=Média, 3=Alta
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 2,
    "nome_requisito": "Novo Pré-requisito",
    "description": "Descrição do pré-requisito",
    "priority": 2,
    "priority_display": "Média"
}
```

##### **4.3. Ver Pré-requisito Específico**
* **Endpoint:** `GET /obstaculos/{obstaculo_id}/prerequisitos/{prerequisito_id}/`
* **Resposta de Sucesso (200 OK):**
```json
{
    "id": 1,
    "nome_requisito": "Variáveis",
    "description": "Aprender variáveis",
    "priority": 1,
    "priority_display": "Baixa"
}
```

##### **4.4. Atualizar um Pré-Requisito**
* **Endpoint:** `PUT /obstaculos/{obstaculo_id}/prerequisitos/{prerequisito_id}/`
* **Corpo da Requisição:**
```json
{
    "nome_requisito": "String (Opcional, não pode ser vazio)",
    "description": "String (Opcional)",
    "priority": "Integer (Opcional)" // 1=Baixa, 2=Média, 3=Alta
}
```

##### **4.5. Deletar um Pré-Requisito**
* **Endpoint:** `DELETE /obstaculos/{obstaculo_id}/prerequisitos/{prerequisito_id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

#### **5. Dependências**

##### **5.1. Listar Dependências**
* **Endpoint:** `GET /dependencias/`
* **Resposta de Sucesso (200 OK):**
```json
[
    {
        "id": 1,
        "requisito_origem": 1,
        "requisito_alvo": 2
    }
]
```

##### **5.2. Criar uma Dependência**
* **Endpoint:** `POST /dependencias/`
* **Descrição:** Cria uma relação onde um pré-requisito (`requisito_alvo`) depende de outro (`requisito_origem`).
* **Corpo da Requisição:**
```json
{
    "requisito_origem": "Integer (ID do pré-requisito, Obrigatório)",
    "requisito_alvo": "Integer (ID do pré-requisito, Obrigatório)"
}
```
* **Resposta de Sucesso (201 Created):**
```json
{
    "id": 2,
    "requisito_origem": 1,
    "requisito_alvo": 2
}
```

##### **5.3. Ver Dependência Específica**
* **Endpoint:** `GET /dependencias/{id}/`
* **Resposta de Sucesso (200 OK):**
```
```

##### **5.5. Deletar uma Dependência**
* **Endpoint:** `DELETE /dependencias/{id}/`
* **Resposta de Sucesso (204 No Content):** Sem corpo na resposta.

---

### **💡 Guia Rápido para o Desenvolvedor Front-End**

* **Fluxo de Trabalho:**
    1.  **Dashboard:** Use `GET /apr/` para listar todas as árvores disponíveis e permitir que o usuário selecione uma.
    2.  **Visualização:** Use `GET /apr/{id}/` para buscar a estrutura da APR selecionada e renderizá-la na interface.
    3.  **Interação:** Use os endpoints de `POST`, `PUT` e `DELETE` para criar, editar e excluir nós da árvore nos seus respectivos níveis (APR, Objetivo, Obstáculo, etc.). O ID do nó pai é passado na URL, simplificando as requisições.

* **Mapeamento de Dados para a UI:**
    * **Prioridades:** Use o campo `priority_display` para exibir o texto ("Alta") e o campo `priority` (ex: 3) para lógica interna ou estilos CSS.
    * **Estrutura de Criação:** Ao criar um item aninhado (ex: um Objetivo), o ID do pai (APR) já está na URL (`/apr/{apr_id}/objetivos/`), o que significa que o campo de relacionamento não precisa ser enviado no corpo da requisição.

---

### **⚠️ Observações Importantes**

1. **Campos obrigatórios e não-brancos:**
   - `username` e `password` são obrigatórios apenas na criação de usuários (POST), não na atualização (PUT).
   - `first_name`, `last_name` e `email` são opcionais, mas se enviados, não podem ser vazios.
   - `nome_apr`, `nome_objetivo`, `nome_obstaculo`, `nome_requisito` são obrigatórios e não podem ser vazios.
   - `priority` é opcional na criação de pré-requisitos (default: 2=Média).
   - `requisito_origem` e `requisito_alvo` são obrigatórios na criação de dependências.
   - `user_id` é obrigatório apenas na criação de APR (POST), não na atualização (PUT).

2. **IDs de Relacionamento:**
   - Os IDs de relacionamento são obtidos da URL, não do body (exceto `user_id` na criação de APR).

3. **Hierarquia da Estrutura:**
   - ARP → Objetivos → Obstáculos → Pré-requisitos → Dependências

4. **Dependências:**
   - Conectam pré-requisitos entre si
   - Podem conectar pré-requisitos de diferentes obstáculos/objetivos/ARPs
   - `requisito_origem` → `requisito_alvo` (origem deve ser concluída antes do alvo)

---

### **💬 Suporte**

Para dúvidas ou problemas com a API, entre em contato com a equipe de desenvolvimento.