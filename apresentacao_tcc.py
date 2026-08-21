import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full", layout_file="layouts/apresentacao_tcc.slides.json")


@app.cell
def _():
    import marimo as mo
    import pathlib

    _IMG = pathlib.Path("tcc_fatec/typst/imagens")

    img_espectro = (_IMG / "espectro.png").resolve().as_uri()
    img_cri = (_IMG / "cri.png").resolve().as_uri()
    img_lamps = (_IMG / "tipos_lampadas.png").resolve().as_uri()
    return img_cri, img_espectro, img_lamps, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Espectrometria de baixo custo

    ## Utilizando fluxo de desenvolvimento moderno para sistemas embarcados

    Centro Estadual de Educação Tecnológica Paula Souza

    Faculdade de Tecnologia da Baixada Santista Rubens Lara

    Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas

    | | |
    |---|---|
    | **Autor** | Lúcio Dias da Silva |
    | **Orientador** | Prof. Me. Rui Silvestrin |
    | **Local** | Santos - SP |
    | **Data** | Maio / 2026 |
    """)
    return


@app.cell(hide_code=True)
def _(img_lamps, mo):
    mo.md(f"""
    # Contexto & Motivação

    ## Da incandescência ao LED

    - A transição para **LED** elevou a eficiência luminosa de **20–30 lm/W** para mais de **210 lm/W** em aplicações especializadas
    - Novos desafios qualitativos: **controle espectral** preciso, temperatura de cor (**CCT**) consistente, alto índice de reprodução de cores (**CRI**) e mitigação de **flicker**

    ## O problema

    - Mercado heterogêneo: especificações divergentes e inconsistência entre fabricantes
    - Falta de **caracterização objetiva e comparativa** de fontes luminosas
    - Equipamentos laboratoriais de alta precisão têm **custo proibitivo** para uso educacional e de pequeno porte

    ![Tipos de lâmpadas e seus níveis de eficiência energética]({img_lamps})
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Objetivos

    ## Geral

    Projetar, desenvolver e validar um sistema de **caracterização espectral** de fontes luminosas que integre:

    - Aquisição de dados via **I2C**
    - Processamento local no **ESP32** com **MicroPython**
    - Apresentação em **interface gráfica acessível**
    - **Comparação objetiva** de fontes por parâmetros espectrais e fotométricos

    ## Específicos

    - Compreender o sensor espectral **AS7341** (arquitetura interna e protocolo I2C)
    - Prototipar o **hardware** (sensor conectado ao ESP32)
    - Desenvolver **drivers** de comunicação em MicroPython
    - Implementar software de **aquisição** com gerenciamento de fluxo e tratamento de exceções
    - Criar interface com **visualizações espectrais e comparativas**
    - Validar por meio de **testes de unidade e integração**
    """)
    return


@app.cell(hide_code=True)
def _(img_cri, img_espectro, mo):
    mo.md(f"""
    # Arquitetura & Tecnologias

    | Camada | Tecnologia | Destaques |
    |---|---|---|
    | **Sensoriamento** | AS7341 (AMS-Osram) | 350–1000 nm, 11 canais (visível, NIR, clear, flicker), I2C |
    | **Plataforma** | ESP32 (Espressif) | Dual-core Xtensa até 240 MHz, Wi-Fi/BLE, criptografia por hardware |
    | **Firmware** | MicroPython 1.27 | Interpretado, REPL, prototipagem ágil |
    | **Web** | Microdot | Servidor assíncrono, WebSockets e SSE |
    | **Interface** | PWA + SVG + TLS | Responsiva, gráficos vetoriais leves, comunicação segura |

    ![Diagrama do espectro eletromagnético]({img_espectro})

    ![Efeito do índice de reprodução de cores (CRI)]({img_cri})
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Funcionalidades & Validação

    ## Requisitos funcionais (resumo)

    - **RF01** — Aquisição espectral de luz via sensor AS7341 (interface I2C)
    - **RF02** — Cálculo de **CCT**, **CRI** e desdobramento espectral a partir dos dados brutos
    - **RF03** — Medição e **comparação objetiva** de múltiplas fontes em uma única sessão
    - **RF04** — Resultados visuais: **espectrograma** e valores calculados na interface
    - **RF05** — Desenvolvimento em **MicroPython 1.27** (portabilidade no ESP32)

    ## Validação & próximos passos

    - **Testes de unidade e integração** de drivers e software de aquisição
    - Validação do sistema em **cenários reais de uso**
    - Comparação com **equipamentos de referência** laboratoriais
    - Contribuição educacional, técnica e econômica: democratizar a análise espectro-fotométrica
    """)
    return


if __name__ == "__main__":
    app.run()