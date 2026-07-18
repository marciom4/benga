---
format: 1080x1080
message: "Uma história de 4 mil anos sobre sonhos e propósito — tão relevante hoje quanto sempre foi."
arc: Hook → Tensão (citação) → Premissa (a história) → Marcas do sonhador → Prova social → CTA
audience: "Leitores de conteúdo devocional/inspiracional cristão, público de língua portuguesa (Brasil)"
mode: collaborative
music: none
---

## Video direction

- **Palette system** (from `frame.md`, preset `coral` remixado): `black` (#0b0806) é o ambiente
  dominante (ink-on-cream em texto claro sobre ele); `coral` (#e2823f, âmbar) é o accent
  primário — usado como region cheia (Frame 3) ou como acento/linha/glow (Frames 1, 2, 6);
  `coral-dark` (#c99a3f, mostarda) é o accent secundário; `cream` (#f4ead9) é o campo claro
  (Frames 4, 5, 6-banda final). Bebas Neue caixa-alta tracked = todo headline/stat; Inter =
  todo corpo/label/atribuição. Ink-on-fire sempre (nunca branco sobre coral).
- **Motion grammar + modelo de revelação**: `power3` long-tail em toda entrada — sem bounce,
  sem overshoot. **Vídeo silencioso**: não há VO para pautar as revelações, então cada Scene é
  pautada pelo próprio texto/elemento em tela — uma frase, uma palavra-chave, um card por vez —
  nunca o quadro inteiro de uma vez (mesmo mecanismo anti-PowerPoint da regra 2 de
  `motion-language.md`, só que o "cue" é o próprio ritmo de leitura em vez da fala). Nada é
  despejado nos primeiros ~25% de cada frame; a segunda metade de cada frame carrega revelação.
- **Ritmo / frames de respiro**: Frame 2 (citação) e Frame 5 (depoimento) são os beats calmos —
  um único movimento restrito e depois quietude total (breather antes/depois dos beats mais
  cinéticos). Frames 1, 3, 4, 6 carregam mais movimento (blocos de texto, numeral, cascata de
  cards, banda final).
- **Lista negativa**: sem bounce/elastic/back.out; sem respiração cíclica em card/texto; sem
  pan/push lento na segunda metade; sem gradiente amaciando um limite de região (exceto o único
  gradiente 135° sancionado, não usado aqui); sem branco sobre coral; sem cantos arredondados
  fora de círculos; sem nav bar / scrollbar / cursor de navegador; sem glow azul-roxo genérico
  de "IA"; sem logotipo real do WhatsApp (usar um ícone genérico de balão de chat, não a marca).

## Frame 1 — Hook: A Jornada de um Sonhador

- scene: Fundo preto com glow âmbar no topo; "A JORNADA DE UM SONHADOR" entra em tipografia grande condensada, autor e tagline abaixo
- voiceover: ""
- duration: 6s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Curiosity gap
- beat: intrigue
- blueprint: kinetic-type-beats (Adapt) — troca o campo plano padrão por um ambiente `black`
  cheio (o chão de marca real do site) com um glow âmbar no topo no lugar da hachura
  diagonal; mantém a assinatura "as palavras são o movimento" em blocos sucessivos.
- focal: none (beat tipográfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Abre com a identidade do livro — o nome, o autor, a promessa ("transformando sonhos em realização") — sem venda ainda.
keyMessage: Este é o livro "A Jornada de um Sonhador".

Scene 1 (0.0–1.2s): fundo `black` cheio; um glow âmbar (coral) sobe suave no topo-centro
(ambient glow bloom); o eyebrow "JOARES MENDES DE FREITAS" (Inter section-label, tracked,
coral) aparece pequeno logo abaixo do glow — Centered, topo do quadro.
Scene 2 (1.2–2.6s): "A" assenta no centro via spring-pop entrance (long-tail suave), pequeno,
acima do slot do título principal.
Scene 3 (2.6–4.2s): "JORNADA" bate em cheio via kinetic beat-slam — Bebas hero-title enorme,
cream, centralizado — o elemento dominante do frame (3–6× o eyebrow).
Scene 4 (4.2–5.2s): "DE UM SONHADOR" revela abaixo via per-word staggered reveal; a palavra
"SONHADOR" fica em coral (âmbar) para ênfase — pilha ainda centralizada.
Scene 5 (5.2–6.0s): a tagline "Transformando sonhos em realização" (Inter body-light, cream)
sobe e assenta abaixo; tudo segura o quadro — só o glow âmbar mantém um jitter sutil limitado
(sine-wave-loop, amplitude baixa); resto estático.

## Frame 2 — Tensão: a citação

- scene: Painel dividido âmbar/preto; citação bíblica em serifada itálica sobre o painel escuro, marca decorativa gigante no painel âmbar
- voiceover: ""
- duration: 7s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-quote.html
- type: pain_point
- persuasion: Authority by association
- beat: tension → curiosity
- blueprint: compose — nenhum shape do banco de roteiro se encaixa numa citação isolada; a
  composição usa o tratamento "Quote Layout" do `frame.md` (painel 40/60 coral+black, giant
  mark, accent-line) como layout, e o vocabulário de movimento para o reveal.
- focal: none (beat tipográfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Estabelece a tensão central do livro — planos humanos vs. propósito maior — com autoridade bíblica, antes de contar a história.
keyMessage: "Em seu coração o homem planeja o seu caminho, mas o Senhor determina os seus passos." — Provérbios 16:9

Scene 1 (0.0–1.0s): split 40/60 assenta — painel `coral` (âmbar) à esquerda com hachura 45°,
painel `black` à direita; uma aspa gigante (giant-mark, 35% ink) se autodesenha traço-a-traço
(SVG self-draw) no painel âmbar.
Scene 2 (1.0–3.2s): no painel preto, a primeira cláusula da citação revela via per-word
staggered reveal — Inter weight-300, itálico (quote-role), cream — "Em seu coração o homem
planeja o seu caminho," — alinhado à esquerda, meio do painel.
Scene 3 (3.2–5.0s): a segunda cláusula revela abaixo, mesmo estilo: "mas o Senhor determina os
seus passos." — a palavra "Senhor" em coral (âmbar) para leve ênfase.
Scene 4 (5.0–6.2s): uma accent-line coral (60×4) se autodesenha acima da atribuição (SVG
self-draw); "PROVÉRBIOS 16:9" (Inter quote-attribution, tracked caps) sobe abaixo dela.
Scene 5 (6.2–7.0s): hold — citação e atribuição assentadas e legíveis; só o giant-mark mantém
um glow ambiente finito e bounded (ambient-glow-bloom, sem loop); resto estático — frame de
respiro.

## Frame 3 — Premissa: uma história de 4 mil anos

- scene: Numeral gigante "4 MIL ANOS" como wallpaper atrás do título "UMA HISTÓRIA DE 4 MIL ANOS. RELEVANTE COMO HOJE.", linha de apoio curta
- voiceover: ""
- duration: 8s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/03-premise.html
- type: product_intro
- persuasion: Negative contrast (antigo ↔ atual)
- beat: intrigue → clarity
- blueprint: dataviz-countup (Adapt) — mantém a assinatura de numeral-herói escalado, mas em
  vez de contar um dado, o "4 MIL ANOS" entra como wallpaper numeral (12% ink) atrás do
  título, no tratamento "Feature Stat" do `frame.md` (ambiente coral cheio + hachura).
- focal: none (beat tipográfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Vira a chave de citação abstrata para a promessa concreta do livro — uma história antiga, ainda viva hoje.
keyMessage: A história tem 4 mil anos e continua relevante hoje.

Scene 1 (0.0–1.4s): ambiente `coral` (âmbar) cheio com hachura 45° sobe; um background-numeral
"4000" (12% ink) desabrocha (ambient glow bloom) morto-centro atrás de onde o título vai
assentar — Centered, ~50%+ do quadro, estabelece escala antes do texto.
Scene 2 (1.4–3.0s): "UMA HISTÓRIA DE" revela via per-word staggered reveal, Bebas ink (preto),
parte superior, tamanho menor.
Scene 3 (3.0–4.6s): "4 MIL ANOS." bate em cheio via kinetic beat-slam / value-scaled counter —
Bebas maior, dominante, centralizado, ink-on-coral — o numeral ganha um pulso de escala único
ao assentar (sem contagem literal, um salto de ênfase).
Scene 4 (4.6–6.4s): "RELEVANTE COMO HOJE." revela abaixo via per-word staggered reveal,
segunda linha, Bebas ink, um pouco menor — completa a pilha do headline.
Scene 5 (6.4–8.0s): hold; o background-numeral mantém só um jitter sutil bounded (amplitude
muito baixa); headline estático e legível.

## Frame 4 — Quatro marcas do sonhador

- scene: Grade 2x2 de quatro cards, cada um com um traço/marca do "sonhador", título "QUATRO MARCAS DO SONHADOR" acima
- voiceover: ""
- duration: 10s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-four-marks.html
- type: feature_showcase
- persuasion: Rule of three (estendida a quatro) / Value stacking
- beat: clarity → aspiration
- blueprint: grid-card-assemble (Adapt) — o tratamento "Three-Column Catalog" do `frame.md`
  (3 cards) é adaptado para uma grade 2×2 de quatro cards, mantendo a assinatura de
  autoassemblagem em cascata e o chrome de borda coral 5px no topo de cada card.
- focal: none (beat tipográfico/gráfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Traduz a história em algo que o leitor pode reconhecer em si mesmo — as marcas de um sonhador.
keyMessage: Quatro marcas definem o sonhador desta história — e talvez do leitor.

Nota de conteúdo: os quatro rótulos abaixo (Fé, Resiliência, Perdão, Propósito) são um
placeholder temático ligado à história bíblica de José — o texto real do card "QUATRO MARCAS
DO SONHADOR" não estava legível na screenshot (ver `capture/extracted/visible-text.txt`).
Ajustar aqui se o usuário enviar o texto exato.

Scene 1 (0.0–1.2s): fundo `black`; "QUATRO MARCAS DO SONHADOR" revela via per-word staggered
reveal, Bebas section-headline, terço superior, centralizado — Centered.
Scene 2 (1.2–3.2s): card 1 "FÉ" se autoassembla no canto superior-esquerdo via cluster→outward
expansion para o slot da grade 2×2 — card cream, borda coral 5px no topo, Bebas card-title +
linha curta Inter.
Scene 3 (3.2–5.2s): card 2 "RESILIÊNCIA" se autoassembla no canto superior-direito, mesma
cascata (~0.3–0.4s de stagger após o assentamento do card 1).
Scene 4 (5.2–7.2s): card 3 "PERDÃO" se autoassembla no canto inferior-esquerdo.
Scene 5 (7.2–9.0s): card 4 "PROPÓSITO" se autoassembla no canto inferior-direito, completando
a grade.
Scene 6 (9.0–10.0s): hold — grade 2×2 completa e legível; sem movimento além de um jitter
sutil bounded na borda coral do card em foco; resto estático.

## Frame 5 — Prova social: o que dizem sobre o livro

- scene: Painel escuro centralizado com um cartão de depoimento de leitor, título "O QUE DIZEM SOBRE O LIVRO" acima
- voiceover: ""
- duration: 7s
- transition_in: crossfade
- status: outline
- src: compositions/frames/05-testimonial.html
- type: social_proof
- persuasion: Social proof
- beat: trust
- blueprint: titlecard-reveal (Reproduce) — card de depoimento único, UM movimento restrito
  (wipe/slide-up) e depois quietude total; o baixo movimento É o payload.
- focal: none (beat tipográfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Valida a promessa com a voz de outros leitores antes do convite final.
keyMessage: Outros leitores já foram transformados por esta jornada.

Nota de conteúdo: o depoimento abaixo é um placeholder genérico (o texto real dos
depoimentos não estava legível na screenshot); nenhum nome de leitor é inventado — a
atribuição fica genérica ("leitor(a)") até o usuário enviar o texto/nome reais.

Scene 1 (0.0–1.0s): fundo `black` sobe; "O QUE DIZEM SOBRE O LIVRO" (Inter section-label +
Bebas bar-title) revela via slide-up crossfade, parte superior, centralizado.
Scene 2 (1.0–3.5s): um único cartão de depoimento desliza para o centro (slide-up) — card
cream, borda coral 5px no topo; o texto "Este livro mudou a forma como vejo meus próprios
sonhos." revela via per-word staggered reveal, Inter body-light, itálico leve.
Scene 3 (3.5–5.0s): a atribuição "— Leitor(a) da primeira edição" sobe abaixo da citação,
Inter quote-attribution, tracked caps, pequena.
Scene 4 (5.0–7.0s): hold — o cartão assenta por completo; nenhum movimento além de um jitter
sutil bounded no brilho da borda coral — frame de respiro.

## Frame 6 — CTA: sua jornada começa aqui

- scene: Campo creme com faixa âmbar inferior; "SUA JORNADA COMEÇA AQUI" centralizado, preço R$ 35,00 e chamada para pedir pelo WhatsApp na faixa
- voiceover: ""
- duration: 10s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/06-cta.html
- type: cta
- persuasion: Risk reversal / Scarcity-free direct ask
- beat: motivation → urgency-to-act
- blueprint: kinetic-type-beats (Adapt) — usa o tratamento "Closing Plate" do `frame.md`
  (campo cream + banda coral inferior) como layout; a linha final assenta em blocos
  sucessivos como no restante do vídeo, mantendo a coerência da assinatura tipográfica.
- focal: none (beat tipográfico/gráfico puro, sem asset_candidates)
- asset_candidates:

narrativeRole: Fecha com o convite direto e o preço — o próximo passo claro para o espectador.
keyMessage: Peça seu exemplar por R$ 35,00 e comece a jornada.

Nota: o ícone de WhatsApp é um balão de chat genérico desenhado em CSS/SVG — nunca o
logotipo real de terceiro (ver lista negativa em Video direction).

Scene 1 (0.0–1.4s): campo `cream` sobe; eyebrow ink "SUA JORNADA" (Inter section-label,
tracked) aparece pequeno, centralizado, parte superior.
Scene 2 (1.4–3.0s): "COMEÇA AQUI" bate em cheio via kinetic beat-slam — Bebas hero-title
grande, ink, centralizado — elemento dominante do campo cream.
Scene 3 (3.0–4.6s): uma accent-line coral se autodesenha abaixo do headline (SVG self-draw),
centralizada.
Scene 4 (4.6–6.4s): a banda `coral` (âmbar) inferior revela via cluster→outward expansion
(wipe de baixo para cima), carregando "R$ 35,00" (Bebas bar-title, ink) à esquerda e "PEÇA
PELO WHATSAPP" (Inter section-label, ink, tracked) à direita — info-bar.
Scene 5 (6.4–8.4s): dentro da banda, um ícone genérico de balão de chat revela via spring-pop
entrance ao lado da chamada, assentando com um leve press-release-spring.
Scene 6 (8.4–10.0s): hold final — a placa de fechamento completa e legível; só um jitter
sutil bounded no brilho da accent-line; último frame do vídeo — este hold É a saída (sem
transição injetada depois dele).
