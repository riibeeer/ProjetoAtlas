# Atlas - Sistema de Gerenciamento de Resíduos

## Descrição
O **Atlas** é um sistema para gerenciamento e monitoramento de resíduos urbanos, projetado para otimizar a coleta, analisar dados e apresentar métricas de eficiência. O sistema permite acompanhar informações detalhadas sobre os resíduos coletados por bairro, tipo, e volume, além de exibir relatórios visuais e gerenciar sensores.

## Funcionalidades Principais
- **Dashboard Interativo**: Exibe gráficos e indicadores-chave sobre os resíduos coletados.
- **Monitoramento em Tempo Real**: Acompanhamento do volume de resíduos coletados por bairro.
- **Relatórios Detalhados**: Geração de relatórios com tabelas, gráficos e exportação de dados.
- **Cadastro de Áreas**: Registro e gerenciamento de áreas de coleta de resíduos.
- **Configuração de Sensores**: Cadastro e manutenção de sensores para monitoramento de resíduos.
- **Central de Notificações e Alertas**: Gerenciamento de eventos críticos e alertas relacionados à coleta.

## Tecnologias Utilizadas
- **Frontend**:
  - **HTML**, **CSS**, **JavaScript**: Para a estrutura e estilo da interface do usuário.
  - **Chart.js**: Para gráficos interativos de análise de dados.
  - **Leaflet.js**: Para visualizações interativas de mapas e localização de áreas de coleta.
  
- **Backend**:
  - **Python**: Para processamento de dados e execução de scripts.
  - **Flask**: Framework para construir o backend do sistema e lidar com rotas simples.
  - **Pandas**: Para manipulação de dados, como leitura e processamento de planilhas Excel.

- **Dados**:
  - **Excel**: Utilizado para armazenar os dados de resíduos, como volumes por tipo e bairro.

- **Outros**:
  - **Streamlit**: Para criar interfaces interativas e gerenciar os relatórios gerados.

## Como Usar

1. **Configuração do Ambiente**:
   - Certifique-se de ter o Python instalado. Você pode verificar com o comando:
     ```bash
     python --version
     ```
   - Crie um ambiente virtual (recomendado):
     ```bash
     python -m venv venv
     ```
   - Ative o ambiente virtual:
     - **Windows**: `venv\Scripts\activate`
     - **Linux/macOS**: `source venv/bin/activate`
   
2. **Instalar as Dependências**:
   - Baixe ou clone o repositório e navegue até o diretório do projeto.
   - Instale todas as dependências do projeto usando o comando:
     ```bash
     pip install -r requirements.txt
     ```

3. **Executando o Sistema**:
   - Para rodar o código do sistema e gerar as interfaces interativas com **Streamlit**, execute os seguintes comandos:
     ```bash
     streamlit run data.py
     streamlit run relatórios.py
     ```
   - O primeiro comando executa o código relacionado aos dados e o segundo comando exibe a interface para visualização dos relatórios.

4. **Abrir o Sistema**:
   - Após executar os comandos acima, você poderá acessar a interface do sistema no navegador em:  
     `http://localhost:8501`

5. **Login (Informação Importante)**:
   - Para acessar o sistema, o usuário precisa ser **admin** e a senha deve ser **1234**.

## Funcionalidades Pendentes

- **Mapa Interativo (Em Desenvolvimento)**: Atualmente, a funcionalidade de mapa interativo usando **Leaflet.js** ou **Folium** não está implementada de forma completa. O objetivo é exibir um mapa interativo que mostre os pontos de coleta de resíduos e a distribuição dos volumes coletados por área. Planejamos integrar dados geoespaciais para isso em uma versão futura.

- **Relatórios em Tempo Real (Em Desenvolvimento)**: A geração de relatórios em tempo real, com dados atualizados automaticamente, ainda está em processo de desenvolvimento. A funcionalidade atual gera relatórios estáticos com base em dados históricos.

- **Integração de Sensores (Em Desenvolvimento)**: O sistema atualmente permite apenas o cadastro de sensores, mas a integração completa com sensores para monitoramento em tempo real ainda precisa ser realizada. Isso permitirá monitorar o status dos sensores em tempo real e gerar alertas automáticos para falhas ou eventos críticos.
