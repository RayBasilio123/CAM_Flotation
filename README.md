# Salva Imagens de Câmeras IP

Este projeto captura frames de câmeras IP e os salva em diretórios especificados. Ele suporta múltiplas câmeras e utiliza threads para processar os streams simultaneamente.

## Funcionalidades

- Captura frames de câmeras IP.
- Salva os frames em diretórios configurados.
- Suporte para múltiplas câmeras.
- Interface gráfica para configuração de URLs e pastas de destino (opcional).

## Pré-requisitos

- Python 3.7 ou superior.
- Bibliotecas necessárias (instale com `pip`):
  ```bash
  pip install opencv-python
  ```

## Caso Queira Criar um Executável

Se desejar criar um executável para o script, siga os passos abaixo:

1. Instale o `pyinstaller`:
   ```bash
   pip install pyinstaller
   ```

2. Gere o executável:
   No terminal, execute o seguinte comando no diretório onde o arquivo `salvaImagensflotacao.py` está localizado:
   ```bash
   pyinstaller --onefile salvaImagensflotacao.py
   ```

3. Localize o executável:
   O executável será gerado na pasta `dist` com o nome `salvaImagensflotacao.exe`.

4. Execute o arquivo:
   Navegue até a pasta `dist` e execute o arquivo `salvaImagensflotacao.exe` para verificar se ele funciona corretamente.

### Observações
- O parâmetro `--onefile` cria um único arquivo executável.
- Certifique-se de que todas as dependências estão instaladas antes de criar o executável.