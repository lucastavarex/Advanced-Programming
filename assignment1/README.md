## Caso de Uso 18 

![image](https://github.com/user-attachments/assets/430eb147-a476-4145-8b53-6b4129921624)


### Descrição

O Caso de Uso 18 detalha o processo de atribuição de um ou mais estudantes (SuperFrogs) a uma solicitação de evento previamente aprovada, realizado por um SuperFrog Coordinator. Essa atribuição pode ser feita de duas formas:

- **Manual**: o coordenador seleciona diretamente os SuperFrogs disponíveis.
- **Automática**: o sistema realiza a seleção com base em critérios como data, localização e preferências dos SuperFrogs.

### Como rodar

```
pip install -r requirements.txt
```

Execute os testes:

```
pytest
```

### Requisitos Funcionais

- O coordenador pode optar por fazer a atribuição manual ou automática.
- SuperFrogs atribuídos devem ser notificados após a confirmação da atribuição.
- O sistema deve evitar conflitos de agendamento entre eventos.
- O sistema deve exibir uma lista de SuperFrogs disponíveis para cada evento.
- O sistema deve permitir que o coordenador visualize todas as solicitações aprovadas.

### Casos de Teste

1. Testar a atribuição automática com base em critérios de elegibilidade.
2. Verificar se a listagem de SuperFrogs disponíveis está correta para uma determinada solicitação.
3. Garantir que o sistema detecta e impede atribuições com sobreposição de horários.
4. Testar a atribuição manual de um SuperFrog a uma solicitação.
5. Verificar se notificações são enviadas corretamente aos SuperFrogs selecionados.
