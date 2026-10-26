# Gera as páginas de serviço e de cidade a partir do index.html: python3 gerar.py
import re, os, json, html
BASE = 'https://desentupidorasf.pages.dev'
idx = open('index.html', encoding='utf-8').read()
css = re.search(r'<style>.*?</style>', idx, re.S).group(0)
header = re.search(r'<header class="top">.*?</header>', idx, re.S).group(0)
footer = re.search(r'<footer>.*?</footer>', idx, re.S).group(0)
tail = idx[idx.index('<a class="wpp wa"'):]
def absol(s):
    s = s.replace('src="img/', 'src="/img/').replace('href="#', 'href="/#')
    return s.replace('href="/#"', 'href="#"')
header, footer, tail = absol(header), absol(footer), absol(tail)

SERV = [
 dict(slug='desentupimento-de-pia', nome='Desentupimento de pia', img='desentupimento-de-pia', kw='desentupimento de pia em São Luís',
  intro='Pia da cozinha ou do banheiro com água parada, descendo devagar ou com mau cheiro? A Desentupidora SF desentope pias em São Luís com máquina profissional, sem desmontar a bancada e sem quebrar azulejo.',
  causas=['Gordura e óleo que endurecem dentro do cano', 'Restos de comida, borra de café e arroz', 'Sabão e resíduos acumulados no sifão', 'Objetos pequenos que caíram no ralo da pia'],
  como='Primeiro identificamos se o entupimento está no sifão ou mais adiante na tubulação. Depois usamos a máquina de cabo rotativo, que vai pelo próprio cano até o ponto entupido e remove a gordura. No final testamos com água corrente.',
  faq=[('Desentupir pia de cozinha quebra o azulejo?', 'Não. O cabo da máquina entra pelo próprio ralo ou pelo sifão. Não é preciso quebrar nada na maioria dos casos.'),
       ('Soda cáustica resolve pia entupida?', 'Pode até aliviar, mas costuma endurecer a gordura, danificar canos de PVC e é perigosa. O ideal é a remoção mecânica com máquina.')]),
 dict(slug='desentupimento-de-ralo', nome='Desentupimento de ralo', img='desentupimento-de-ralo', kw='desentupimento de ralo em São Luís',
  intro='Ralo de banheiro, box, área de serviço ou quintal voltando água e com mau cheiro? A Desentupidora SF desentope ralos em São Luís sem quebrar o piso.',
  causas=['Cabelo e sabonete formando uma bola no cano', 'Areia e terra levadas pela água', 'Fiapos de roupa da máquina de lavar', 'Sifão do ralo sujo, que causa o mau cheiro'],
  como='Abrimos a grelha, limpamos o sifão do ralo e passamos a máquina desentupidora pela tubulação até a caixa de passagem. Assim o ralo volta a escoar e o cheiro vai embora.',
  faq=[('Por que o ralo do banheiro tem mau cheiro?', 'Geralmente o sifão está sujo ou seco, ou há resíduos parados no cano. A limpeza com máquina resolve as duas coisas.'),
       ('Precisa quebrar o piso para desentupir ralo?', 'Na maioria dos casos, não. A máquina passa pelo próprio ralo.')]),
 dict(slug='desentupimento-de-vaso-sanitario', nome='Desentupimento de vaso sanitário', img='desentupimento-de-vaso-sanitario', kw='desentupimento de vaso sanitário em São Luís',
  intro='Vaso entupido, transbordando ou com a descarga fraca? A Desentupidora SF desentope vasos sanitários em São Luís, na maioria das vezes sem tirar a louça do lugar.',
  causas=['Papel higiênico em excesso', 'Lenço umedecido, absorvente e fio dental', 'Objetos que caíram no vaso', 'Entupimento na rede de esgoto depois do vaso'],
  como='Usamos uma mola própria para vaso, que passa pela curva da louça sem riscar. Se o entupimento estiver mais à frente, seguimos com a máquina pela rede de esgoto até a caixa.',
  faq=[('Vaso entupido precisa trocar a louça?', 'Quase nunca. A mola própria para vaso resolve sem retirar a louça na maioria dos casos.'),
       ('Por que o vaso entope toda hora?', 'Pode ser algo preso na curva da louça ou um problema na rede de esgoto. Vale fazer o desentupimento completo, não só da louça.')]),
 dict(slug='desentupimento-de-esgoto', nome='Desentupimento de esgoto', img='desentupimento-de-esgoto', kw='desentupimento de esgoto em São Luís',
  intro='Esgoto voltando, caixa transbordando ou cheiro forte no quintal? A Desentupidora SF desentope redes de esgoto em casas, condomínios e empresas de São Luís.',
  causas=['Gordura e resíduos acumulados ao longo dos anos', 'Raízes de árvores que entram na tubulação', 'Lixo jogado em vasos e ralos', 'Caixas de passagem e de inspeção cheias'],
  como='Abrimos as caixas de inspeção, localizamos o trecho entupido e usamos máquina de cabo rotativo, que alcança longas distâncias sem quebrar o piso. No final, verificamos o escoamento em todas as caixas.',
  faq=[('Vocês atendem esgoto de condomínio e empresa?', 'Sim. Atendemos residências, condomínios, restaurantes, lojas e empresas.'),
       ('A máquina alcança tubulações longas?', 'Sim. O cabo rotativo chega a trechos longos da rede, sem precisar abrir o piso.')]),
 dict(slug='limpeza-de-caixa-de-gordura', nome='Limpeza e desentupimento de caixa de gordura', img='limpeza-caixa-de-gordura', kw='limpeza de caixa de gordura em São Luís',
  intro='Caixa de gordura cheia, transbordando ou com cheiro forte? A Desentupidora SF faz limpeza e desentupimento de caixa de gordura em São Luís para casas, restaurantes e condomínios.',
  causas=['Óleo e gordura da cozinha', 'Restos de comida que descem pela pia', 'Falta de limpeza periódica', 'Cano de saída da caixa entupido'],
  como='Retiramos a gordura acumulada, limpamos a caixa e desentupimos os canos de entrada e de saída. Depois orientamos sobre o intervalo ideal para a próxima limpeza.',
  faq=[('De quanto em quanto tempo limpar a caixa de gordura?', 'Em casas, a cada poucos meses. Em restaurantes e cozinhas industriais, com mais frequência, conforme o volume de uso.'),
       ('Caixa de gordura cheia causa mau cheiro?', 'Sim. Além do cheiro, ela faz a pia entupir e pode transbordar.')]),
 dict(slug='desentupimento-de-calhas', nome='Desentupimento de calhas', img='desentupimento-de-calhas', kw='desentupimento de calhas em São Luís',
  intro='Calha transbordando na chuva ou água escorrendo pela parede? A Desentupidora SF limpa e desentope calhas e condutores em São Luís antes que vire infiltração.',
  causas=['Folhas e galhos de árvores', 'Sujeira e areia levadas pelo vento', 'Ninhos de passarinho', 'Condutor (cano de descida) entupido'],
  como='Retiramos folhas e sujeira da calha, desentupimos o condutor de descida e testamos com água para garantir que tudo escoa antes da próxima chuva.',
  faq=[('Quando limpar as calhas em São Luís?', 'O ideal é antes do período de chuvas, que vai de janeiro a junho, e sempre que houver árvores perto do telhado.'),
       ('Calha entupida causa infiltração?', 'Sim. A água transborda e escorre pela parede e pelo forro.')]),
]
CID = [
 dict(slug='desentupidora-sao-luis', nome='São Luís', bairros=['Renascença','Calhau','Ponta d\'Areia','Cohama','Turu','Cohab','Cohatrac','Vinhais','Olho d\'Água','Centro','São Francisco','Angelim','Anil','Cohafuma','Jardim Renascença','Bequimão','Cidade Operária','São Cristóvão','Ponta do Farol','Planalto Turu','Vicente Fialho','Araçagi']),
 dict(slug='desentupidora-sao-jose-de-ribamar', nome='São José de Ribamar', bairros=['Centro de Ribamar','Araçagi','Panaquatira','Maiobinha','Jardim Tropical','Vila Sarney Filho','Parque Vitória','Cohatrac IV']),
 dict(slug='desentupidora-paco-do-lumiar', nome='Paço do Lumiar', bairros=['Maiobão','Pindaí','Mojó','Iguaíba','Paranã','Vila São José','Residencial Primavera']),
 dict(slug='desentupidora-raposa', nome='Raposa', bairros=['Centro da Raposa','Vila Bom Viver','Inhaúma','Cumbique','Vila Maresia']),
]

def page(path, title, desc, h1, body, crumbs, extra_ld):
    url = f'{BASE}/{path}/'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(crumbs)]}] + extra_ld}
    bc = ' › '.join(f'<a href="{u}">{n}</a>' if i < len(crumbs)-1 else n for i, (n, u) in enumerate(crumbs))
    doc = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="geo.region" content="BR-MA"><meta name="theme-color" content="#0a2a6e">
<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/img/og.jpg">
<link rel="icon" href="/img/favicon.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,500;0,600;0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
{css}
<style>.ph{{padding:56px 0 110px}}.ph .wrap{{display:block;padding-top:0;padding-bottom:0}}.bc{{font-size:14px;opacity:.85;margin-bottom:14px}}.bc a{{text-decoration:underline}}
.art{{max-width:860px;margin:0 auto}}.art h2{{margin-top:44px}}.art p{{font-size:17px;color:#33415c;margin-top:12px}}.art ul{{margin:14px 0 0 0}}.links{{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}}.links a{{background:#fff;border:1px solid var(--line);padding:9px 16px;border-radius:999px;font-weight:700;font-size:14.5px;color:var(--blue)}}.links a:hover{{border-color:var(--orange);color:var(--orange)}}</style>
</head>
<body>
{header}
<main>
<section class="hero ph"><div class="wrap"><div class="bc">{bc}</div><h1>{h1}</h1><p class="lead">{html.escape(desc)}</p>
<div class="ctas"><a class="btn btn-wpp wa" href="#">Pedir orçamento no WhatsApp</a><a class="btn btn-ghost" href="tel:+5598989153929">Ligar: (98) 98915-3929</a></div></div></section>
<section><div class="wrap art">{body}</div></section>
</main>
{footer}
{tail}'''
    os.makedirs(path, exist_ok=True)
    open(f'{path}/index.html', 'w', encoding='utf-8').write(doc)
    return url

empresa = {"@id": f"{BASE}/#empresa"}
links_serv = '<div class="links">' + ''.join(f'<a href="/{s["slug"]}/">{s["nome"]}</a>' for s in SERV) + '</div>'
links_cid = '<div class="links">' + ''.join(f'<a href="/{c["slug"]}/">Desentupidora em {c["nome"]}</a>' for c in CID) + '</div>'
urls = [BASE + '/']

for s in SERV:
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in s['faq'])
    body = f'''<img src="/img/{s['img']}.webp" alt="{s['nome']} em São Luís – Desentupidora SF" width="800" height="500" style="border-radius:22px;width:100%;height:auto">
<h2>{s['nome']} em São Luís <span>sem quebra-quebra</span></h2><p>{s['intro']}</p>
<h2>Principais <span>causas</span></h2><ul class="list">{''.join(f'<li><span>{c}</span></li>' for c in s['causas'])}</ul>
<h2>Como fazemos o <span>serviço</span></h2><p>{s['como']}</p>
<div class="band" style="margin-top:40px"><div><h2>Orçamento grátis pelo WhatsApp</h2><p>Mande uma foto ou vídeo do problema.</p></div><a class="btn wa" href="#" data-s="{s['nome'].lower()}">Chamar agora</a></div>
<h2>Dúvidas sobre <span>{s['nome'].lower()}</span></h2><div class="faq" style="margin-top:18px">{faq}</div>
<h2>Onde <span>atendemos</span></h2><p>{s['nome']} em São Luís, São José de Ribamar, Paço do Lumiar e Raposa.</p>{links_cid}
<h2>Outros <span>serviços</span></h2>{links_serv}'''
    ld = [{"@type": "Service", "name": s['nome'], "serviceType": s['nome'], "provider": empresa, "image": f"{BASE}/img/{s['img']}.webp",
           "areaServed": [{"@type": "City", "name": c['nome']} for c in CID]},
          {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s['faq']]}]
    urls.append(page(s['slug'], f"{s['nome']} em São Luís MA | Desentupidora SF", f"{s['nome']} em São Luís – MA com equipamento profissional e sem quebra-quebra. Orçamento grátis pelo WhatsApp (98) 98915-3929.",
                     f"{s['nome']} em <em>São Luís</em>", body, [('Início', '/'), (s['nome'], f"/{s['slug']}/")], ld))

for c in CID:
    body = f'''<h2>Desentupidora em {c['nome']} <span>com orçamento grátis</span></h2>
<p>A Desentupidora SF atende {c['nome']} com desentupimento de pias, ralos, vasos sanitários, esgoto, caixas de gordura e calhas. Usamos máquinas profissionais que chegam ao entupimento pela própria tubulação, sem quebrar piso nem parede.</p>
<p>É só chamar no WhatsApp, mandar uma foto ou vídeo do problema e receber o orçamento sem compromisso.</p>
<h2>Serviços em <span>{c['nome']}</span></h2>{''.join(f'<p><a href="/{s["slug"]}/" style="color:var(--orange);font-weight:800">{s["nome"]} em {c["nome"]}</a>: {s["intro"].split("?")[0]}?</p>' for s in SERV)}
<h2>Bairros atendidos em <span>{c['nome']}</span></h2><div class="bairros" style="justify-content:flex-start">{''.join(f'<span>{b}</span>' for b in c['bairros'])}</div>
<div class="band" style="margin-top:40px"><div><h2>Entupiu em {c['nome']}?</h2><p>Fale agora com a Desentupidora SF: (98) 98915-3929</p></div><a class="btn wa" href="#">Chamar no WhatsApp</a></div>
<h2>Outras <span>cidades</span></h2>{links_cid}'''
    ld = [{"@type": "Service", "name": f"Desentupidora em {c['nome']}", "serviceType": "Desentupimento", "provider": empresa, "areaServed": {"@type": "City", "name": c['nome']}}]
    urls.append(page(c['slug'], f"Desentupidora em {c['nome']} MA | Desentupidora SF", f"Desentupidora em {c['nome']} – MA: pia, ralo, vaso, esgoto, caixa de gordura e calhas sem quebra-quebra. Orçamento grátis: (98) 98915-3929.",
                     f"Desentupidora em <em>{c['nome']}</em>", body, [('Início', '/'), (f"Desentupidora em {c['nome']}", f"/{c['slug']}/")], ld))

open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    ''.join(f'<url><loc>{u}</loc><changefreq>monthly</changefreq><priority>{"1.0" if u == BASE + "/" else "0.8"}</priority></url>' for u in urls) + '</urlset>\n')
print(len(urls), 'URLs')
