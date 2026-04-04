# Finance Control — Backend

API REST para controle financeiro pessoal. Fornece autenticação JWT, gerenciamento de contas, transações e categorias com isolamento completo de dados por usuário.

> Frontend React disponível em: [finance-control--web](https://github.com/MatheusSlvRibeiro/finance-control)

---

## Funcionalidades

- Autenticação com JWT (SimpleJWT — access + refresh token)
- Cadastro de usuários com onboarding automático (contas e categorias padrão criadas via signal)
- CRUD completo de contas, transações e categorias
- Todos os dados isolados por usuário autenticado (sem vazamento entre contas)
- Soft delete com `deleted_at` em todos os modelos
- UUID como chave primária em todos os modelos
- Documentação automática via Swagger e ReDoc
- Filtros, busca e ordenação em todos os endpoints

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | Django 5.2 + Django REST Framework |
| Autenticação | djangorestframework-simplejwt |
| Documentação | drf-yasg (Swagger/ReDoc) |
| Filtros | django-filter |
| Banco (dev) | SQLite |
| Banco (prod) | PostgreSQL |
| Servidor (prod) | Gunicorn + Uvicorn |
| Deploy | Docker |

---

## Arquitetura

```
finance-control--api/
├── backend/          # Configuração global (settings, urls, wsgi, asgi)
├── core/
│   └── mixins/       # BaseModel (UUID + soft delete + timestamps)
│                     # CreateAllowAnyMixin, CreateSerializerMixin
│                     # swagger_viewset_methods (decoradores automáticos)
├── users/            # Usuário customizado (login por email), signal de onboarding
├── accounts/         # Contas financeiras (checking, wallet, investments)
├── categories/       # Categorias com tipo, cor e ícone
└── transactions/     # Transações vinculadas a contas
```

### Decisões de arquitetura

**BaseModel com UUID e soft delete**
Todos os modelos herdam de `BaseModel`, que combina `UUIDModel` (UUID como PK) e `TimeStampedModel` (`created_at`, `updated_at`). O método `.delete()` foi sobrescrito para soft delete via `deleted_at`, com `.restore()` e `.hard_delete()` disponíveis.

**Isolamento de dados por usuário**
Todas as ViewSets sobrescrevem `get_queryset()` filtrando por `request.user`. O atributo de classe `queryset = Model.objects.none()` é mantido apenas para compatibilidade com a geração de schema do drf-yasg.

**Onboarding automático via signal**
Ao criar um novo usuário, o signal `post_save` cria automaticamente (dentro de `transaction.on_commit`) as contas padrão para cada tipo e as 9 categorias definidas em `categories/defaults.py`. O uso de `on_commit` garante que os objetos só são criados após a transação do usuário ser confirmada.

**CreateAllowAnyMixin**
Permite que o endpoint `POST /api/v1/users/` seja acessado sem autenticação (para cadastro), enquanto todos os outros métodos exigem `IsAuthenticated`. Reutilizado em todas as ViewSets que precisam desse padrão.

---

## Endpoints

| Recurso | Base URL | Autenticação |
|---|---|---|
| Obter token JWT | `POST /api/token/` | Não |
| Renovar token | `POST /api/token/refresh/` | Não |
| Usuários | `/api/v1/users/` | Não (POST) / Sim (demais) |
| Contas | `/api/v1/accounts/` | Sim |
| Categorias | `/api/v1/categories/` | Sim |
| Transações | `/api/v1/transactions/` | Sim |
| Swagger UI | `/swagger/` | Não |
| ReDoc | `/redoc/` | Não |
| Admin | `/admin/` | Sim (staff) |

---

## Rodando localmente

### Pré-requisitos

- Python 3.13+
- Git

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/MatheusSlvRibeiro/finance-control-backend.git
cd finance-control-backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com sua SECRET_KEY e configurações locais
```

### Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

```env
# Gere uma chave com:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=sua-secret-key-aqui

# True apenas em desenvolvimento local
DEBUG=True

# Separados por vírgula
ALLOWED_HOSTS=127.0.0.1,localhost

# Usado apenas quando DEBUG=False, separados por vírgula
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

### Banco de dados e execução

```bash
# Aplica as migrações existentes
python manage.py migrate

# Cria superusuário (opcional, para acessar /admin/)
python manage.py createsuperuser

# Inicia o servidor
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

Swagger: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### Exemplo de autenticação

```bash
# Obter token JWT (login por email)
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@example.com", "password": "suasenha"}'

# Usar o token nas requisições
curl http://localhost:8000/api/v1/accounts/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Rodando com Docker

```bash
docker-compose up --build
```

O banco PostgreSQL e a aplicação sobem juntos. As variáveis de ambiente devem ser configuradas no `docker-compose.yaml` ou em um arquivo `.env`.

---

## Testes

```bash
python manage.py test
```

---

## Autor

**Matheus Ribeiro** — Desenvolvedor Fullstack

- GitHub: [MatheusSlvRibeiro](https://github.com/MatheusSlvRibeiro)
- LinkedIn: [matheusslvribeiro](https://www.linkedin.com/in/matheusslvribeiro/)
