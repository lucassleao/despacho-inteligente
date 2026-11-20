# 🎯 Perguntas de entrevista: Estágio AI Engineer

Guia vivo: a cada aula, entram perguntas novas. Respostas escritas **do jeito que você falaria** na entrevista, citando o seu projeto sempre que der.

> **Como usar:** leia a pergunta, tente responder **em voz alta** sem olhar, e só depois confira. Entrevista é falar, não ler.

> **Dica geral:** a melhor resposta segue o formato **conceito → exemplo do meu projeto → por que importa**. Mostra que você não só decorou, mas usou.

---

## 1. Sobre o seu projeto (vão perguntar com certeza)

### ❓ "Me fala de um projeto seu."
**Resposta:**
> "Construí o Despacho Inteligente, um simulador de entregas em Python. O problema que eu quis resolver: quando a comida atrasa na cozinha, o entregador fica parado esperando no balcão, e isso é tempo perdido pra ele e pra plataforma. O sistema detecta que o pedido vai atrasar e recomenda uma entrega curta no caminho, que ele faz e volta a tempo de pegar o pedido atrasado.
> Comecei pela modelagem do domínio, depois a geografia (distância com Haversine), e tudo com testes automatizados e versionado no GitHub. A ideia é comparar o mesmo dia simulado com e sem o sistema e medir quantos minutos parados foram economizados."

**Por que funciona:** problema real → solução → como fez → como mede. Nessa ordem.

### ❓ "Por que você escolheu esse problema?"
> "Porque é um problema de negócio real em delivery: o tempo ocioso do entregador custa dinheiro, aumenta o tempo de entrega e reduz o ganho dele. Eu queria um projeto que juntasse otimização, ML e IA generativa num caso que faz sentido pra empresa, e não só treinar um modelo num dataset pronto."

### ❓ "Qual foi a maior dificuldade?"
Escolha algo **verdadeiro** que aconteceu com você. Exemplo:
> "No começo, configurar o ambiente: ambiente virtual, PATH do Windows, política de scripts do PowerShell, autenticação do Git. Aprendi a ler mensagens de erro de baixo pra cima e a conferir o estado (`git status`) em vez de repetir comandos às cegas."

**Por que funciona:** entrevistador de estágio quer ver **como você aprende**, não que você nunca erra.

---

## 2. Python (base de qualquer vaga de AI Engineer)

### ❓ "O que é uma dataclass e por que usar?"
> "É um decorador que gera automaticamente `__init__`, `__repr__` e `__eq__` a partir dos campos declarados com tipo. Uso no projeto pra modelar `Ponto`, `Pedido` e `Entregador`: o código fica curto e a estrutura dos dados fica explícita."

### ❓ "Pra que serve `frozen=True`?"
> "Torna o objeto imutável: depois de criado, não dá pra alterar os campos. Usei no `Ponto` porque uma coordenada é um **valor**, como o número 5: não faz sentido ela mudar. Quando o entregador se move, ele recebe um ponto novo. Isso evita bugs em que um objeto compartilhado é alterado sem querer em outro lugar do código. Bônus: objetos imutáveis podem ser chave de dicionário."

### ❓ "O que é `@property`?"
> "Transforma um método num atributo calculado na hora do acesso. No meu `Entregador`, `livre` é uma property que retorna `pedido_atual is None`. Se fosse um campo separado, poderia ficar contraditório com o `pedido_atual`. Assim existe uma **fonte única da verdade**."

### ❓ "Por que usar Enum em vez de strings?"
> "Strings aceitam qualquer valor, então um erro de digitação como `'Pronto'` vs `'pronto'` vira um bug silencioso. Com Enum, um valor inválido dá erro na hora e o editor autocompleta. No projeto, o status do pedido é um Enum."

### ❓ "Qual a diferença entre `is` e `==`?"
> "`==` compara **valor**; `is` compara **identidade**, se é o mesmo objeto na memória. Pra `None`, o recomendado é `is None`, porque `None` é um objeto único."

### ❓ "O que são type hints? O Python obriga?"
> "São anotações de tipo como `def f(a: Ponto) -> float`. O Python **não** obriga em tempo de execução, mas ferramentas como Pylance e mypy usam pra achar erros antes de rodar. Em time grande, isso vira documentação viva."

### ❓ "Por que `0.1 + 0.2 != 0.3`?"
> "Porque números decimais são guardados em binário (ponto flutuante) e alguns, como 0.1, não têm representação exata. Por isso, nos testes, uso `pytest.approx` pra comparar floats com tolerância."

### ❓ "O que é list comprehension?"
> "Um jeito conciso de criar uma lista a partir de outra: `[p.id for p in pedidos if p.atrasado]`. Uso quando a lógica é simples; quando fica complexa, prefiro um `for` normal, porque legibilidade vem primeiro."

---

## 3. Engenharia de software (diferencia estagiário bom)

### ❓ "Por que escrever testes?"
> "Pra mudar o código com confiança. Se amanhã eu trocar a distância em linha reta por rotas reais, os testes me dizem na hora se quebrei algo. No meu projeto, testo propriedades como 'distância de um ponto pra ele mesmo é zero' e 'a distância é simétrica', além de um valor conhecido (SP–Rio ≈ 360 km)."

### ❓ "Como você sabe que um teste está testando algo de verdade?"
> "Faço ele falhar de propósito pelo menos uma vez. Um teste que nunca falha pode estar testando nada."

### ❓ "O que é ambiente virtual e por que usar?"
> "É um Python isolado por projeto, com as suas próprias bibliotecas. Evita que um projeto que precisa da versão 1 de uma biblioteca quebre outro que precisa da versão 2. As dependências ficam listadas no `requirements.txt`, então qualquer pessoa recria o mesmo ambiente."

### ❓ "Por que o `.venv` não vai pro Git?"
> "Porque é grande, específico do sistema operacional e recriável a partir do `requirements.txt`. No Git vai só o que é código-fonte e configuração."

### ❓ "Explique add, commit e push."
> "`add` coloca as mudanças na área de preparação, ou seja, escolho o que vai entrar. `commit` cria uma versão salva no histórico local, com uma mensagem explicando a mudança. `push` envia os commits pro repositório remoto, como o GitHub."

### ❓ "Errou algo que já está no GitHub. O que faz?"
> "Crio um commit novo corrigindo. Num repositório compartilhado, não reescrevo o histórico, porque isso atrapalha quem já baixou. Aconteceu comigo: nomeei o README errado e corrigi com `git mv` e um commit novo."

### ❓ "O que é encapsulamento? Dê um exemplo."
> "Esconder **como** algo funciona atrás de uma interface simples. No projeto, todo mundo chama `tempo_viagem_min(a, b)` sem saber que por dentro é linha reta × 1,3. Quando eu trocar por rotas reais do OpenStreetMap, só essa função muda."

---

## 4. Machine Learning e dados (centrais pra vaga)

### ❓ "O que é data leakage (vazamento de dados)?"
> "É quando o modelo, no treino, tem acesso a uma informação que não estaria disponível no momento real da previsão. Ele parece ótimo no teste e fracassa em produção. No meu projeto, o pedido tem um campo `pronto_em` com a hora real em que a comida fica pronta. O algoritmo de despacho **não pode** usar esse campo, porque na vida real ninguém sabe isso de antemão. Ele precisa **estimar** a partir do histórico."

**⭐ Essa é uma das perguntas mais valiosas pra você: tem exemplo real no seu código.**

### ❓ "Por que usar uma seed fixa?"
> "Reprodutibilidade. Com a mesma seed, a simulação gera exatamente o mesmo dia. Isso me permite comparar 'com o sistema' e 'sem o sistema' nas mesmas condições: qualquer diferença vem do algoritmo, não da sorte."

### ❓ "Por que dados sintéticos? Quais as limitações?"
> "Não tenho acesso aos dados reais de uma empresa de delivery, então gero dados realistas pra validar a lógica. A limitação é que o resultado depende das premissas que eu escolhi, como 25% de pedidos atrasando. Por isso deixo essas premissas explícitas e configuráveis, e o ideal seria calibrar com dados reais."

### ❓ "Qual a diferença entre regressão e classificação?"
> "Regressão prevê um **número** (quantos minutos o pedido vai atrasar). Classificação prevê uma **categoria** (vai atrasar mais de 10 min: sim ou não). No meu projeto, prever o tempo de preparo é regressão."

### ❓ "Como você avaliaria um modelo de previsão de tempo de entrega?"
> "Com MAE (erro absoluto médio), porque é fácil de explicar: 'erra em média 3 minutos'. Também olharia o erro **por faixa**, já que errar pra menos (prometer 20 min e entregar em 35) é pior pro cliente que errar pra mais. E sempre separaria treino e teste **no tempo**: treino com o passado e testo com o futuro, pra não ter vazamento."

### ❓ "O que é overfitting?"
> "Quando o modelo decora os dados de treino em vez de aprender o padrão, e vai mal em dados novos. Dá pra detectar quando o erro de treino é muito menor que o de validação. Combate-se com mais dados, modelos mais simples, regularização e validação cruzada."

---

## 5. O problema de negócio (delivery e logística)

### ❓ "Quais métricas importam num sistema de despacho?"
> "Pro cliente: tempo de entrega e se chegou no prazo prometido. Pro entregador: ganhos por hora e tempo ocioso. Pra plataforma: entregas por hora e custo por entrega. No meu projeto, a métrica principal é minutos de entregador parado, e a métrica de proteção é o atraso médio: não adianta reduzir a espera se os clientes começarem a receber mais tarde."

**Conceito-chave:** sempre que otimizar uma métrica, defina uma **métrica de proteção** (*guardrail*) pra não piorar outra.

### ❓ "Como seu sistema decide se recomenda uma viagem extra?"
> "Calcula o tempo do desvio: ir até o outro restaurante, entregar e voltar. Compara com a folga até o pedido original ficar pronto. Só recomenda se o desvio couber na folga, com uma margem de segurança, e se a comida do segundo pedido não ficar tempo demais na bag. Entre as opções válidas, escolhe a que mais reduz o tempo parado."

### ❓ "E se a previsão de atraso estiver errada?"
> "Esse é o risco principal. Se o sistema achar que vai atrasar 20 min e a comida ficar pronta em 5, o entregador está longe e o cliente original espera. Por isso: uso uma margem de segurança, posso recomendar só quando a confiança da previsão for alta, e meço na simulação o caso ruim, não só a média."

### ❓ "Como escalaria isso pra milhares de entregadores?"
> "Não dá pra testar todas as combinações. Primeiro filtraria por proximidade (só pedidos num raio de poucos km, usando índice espacial). Depois usaria uma heurística gulosa ou um solver de roteamento como o OR-Tools. E processaria por região, em paralelo."

---

## 6. IA generativa / LLMs (muito valorizado hoje)

### ❓ "O que é RAG?"
> "Retrieval-Augmented Generation. Antes de o LLM responder, busco documentos relevantes, por exemplo os pratos de um cardápio, e coloco no prompt. Assim o modelo responde com base em dados reais e atualizados, sem precisar ser retreinado, e alucina menos."

### ❓ "O que são embeddings?"
> "Vetores de números que representam o significado de um texto. Textos parecidos ficam com vetores próximos. Isso permite buscar 'algo leve pro almoço' e encontrar 'salada de quinoa', mesmo sem palavras em comum."

### ❓ "O que é tool calling / agente?"
> "É quando o LLM, em vez de só gerar texto, decide chamar funções que eu disponibilizo, como `buscar_pratos(preco_max=40)`, recebe o resultado e continua o raciocínio. No meu projeto, o plano é que o assistente explique as recomendações ao entregador e consulte o motor de despacho."

### ❓ "Como avaliar se um LLM está respondendo bem?"
> "Criando um conjunto de perguntas de teste com respostas esperadas e medindo a taxa de acerto. Pra respostas abertas, dá pra usar critérios objetivos (citou um prato que existe? respeitou o preço?) ou um segundo LLM como avaliador, validado por amostragem humana."

---

## 7. Comportamentais

### ❓ "Por que o iFood?"
Pesquise antes e **fale com as suas palavras**. Estrutura:
> "Porque [algo específico que você leu sobre a empresa/tecnologia] e porque o tipo de problema que me interessa, de logística e IA aplicada a algo que milhões de pessoas usam, é o centro do negócio de vocês. Meu projeto pessoal é justamente sobre isso."

### ❓ "Fale de uma vez em que você travou e como resolveu."
Use o método **STAR**: **S**ituação, **T**arefa, **A**ção, **R**esultado. Exemplo real seu:
> "**S:** meu `git push` terminava sem erro mas não enviava nada. **T:** precisava publicar o código. **A:** em vez de repetir o comando, conferi o estado com `git status`, vi que estava 'ahead 1' e investiguei a autenticação. **R:** descobri que era a autenticação do terminal do editor; corrigi a configuração e aprendi a verificar o estado antes de repetir comandos."

### ❓ "Onde você quer chegar?"
> "Quero me aprofundar em ML aplicado a produto: colocar modelos em produção, medir impacto real e iterar. O estágio é o lugar pra aprender isso com quem faz em escala."

---

## 8. Simulação e dados sintéticos (aula da `cidade.py`)

### ❓ "Por que criar um `random.Random(seed)` próprio em vez de usar `random.random()`?"
> "O `random` do módulo é **global**: qualquer outra parte do código que sorteie algo muda a sequência, e a simulação deixa de ser reproduzível. Um gerador próprio, criado com a seed e passado adiante como parâmetro, garante que a mesma seed gera sempre o mesmo dia. Isso também facilita testar."

### ❓ "Como sortear pontos uniformemente dentro de um círculo?"
> "Sorteio um ângulo uniforme e uma distância igual a `raio × sqrt(u)`, com `u` uniforme entre 0 e 1. Sem a raiz, os pontos se concentram no centro, porque a área de um anel cresce com o raio: a borda precisa receber mais pontos que o miolo."

### ❓ "Como você modelou os atrasos da cozinha? Por que assim?"
> "Com uma **mistura de distribuições**: 75% dos pedidos seguem uma normal centrada na média do restaurante (variação pequena) e 25% recebem um atraso grande, uniforme entre 8 e 25 min. Na vida real, a maioria dos pedidos é normal e uma minoria atrasa muito (cozinha lotada). Uma distribuição só não captura essas duas situações."

### ❓ "O que você faz quando o sorteio gera um valor impossível?"
> "Coloco uma **trava de sanidade**. Por exemplo, `max(5, preparo)`: a normal pode sortear um preparo negativo, o que não existe. Dados impossíveis na simulação viram bugs estranhos lá na frente."

### ❓ "Por que converter km em graus de um jeito diferente pra latitude e longitude?"
> "Um grau de latitude vale sempre ~111 km. Já o grau de longitude encolhe conforme se afasta do Equador, por um fator `cos(latitude)`. Em São Paulo, ele vale ~102 km."

---

## ✅ Checklist antes da entrevista
- [ ] Sei explicar meu projeto em **1 minuto** e em **5 minutos**
- [ ] Tenho o link do GitHub com README bom e testes passando
- [ ] Sei responder data leakage com o exemplo do `pronto_em`
- [ ] Tenho 2 histórias STAR reais prontas
- [ ] Li sobre a empresa e tenho 2 perguntas pra fazer ao entrevistador (ex.: "Como o time mede o impacto de um modelo em produção?")

---

*Atualizado a cada aula. Próximas perguntas: simulação de eventos, algoritmo de despacho, comparação A/B.*
