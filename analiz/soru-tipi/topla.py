# Kullanım: python3 topla.py <bu klasör>  → TOPLU-SAYIMLAR.md dosyasını yeniden üretir.
import csv,collections,sys,os,re
T=sys.argv[1]
YRS=["2021","2022","2023","2024","2025"]
rows=[]
for y in YRS:
    p=f"{T}/{y}-alt-tip-etiketleri.csv"
    if not os.path.exists(p): continue
    for r in csv.DictReader(open(p,encoding="utf-8")):
        r={k.strip():(v or "").strip() for k,v in r.items()}
        rows.append(r)
ys=sorted({r["yil"] for r in rows})
out=[]
P=out.append
P(f"# Toplu sayımlar ({len(rows)} soru, yıllar: {', '.join(ys)})\n")
AN={"O":"Olumsuz","D":"Düz","Ö":"Öncüllü","G":"Doğru","V":"Vaka","K":"Kavram","B":"Boşluk","E":"Eşleştirme","S":"Sıralama","H":"Hesap"}
# ana tip x yıl
P("## Ana tip × yıl\n\n| Ana tip | "+" | ".join(ys)+" | Top |\n|---|"+"---|"*(len(ys)+1))
for a in AN:
    c=[sum(1 for r in rows if r["ana_tip"]==a and r["yil"]==y) for y in ys]
    P(f"| {a} {AN[a]} | "+" | ".join(map(str,c))+f" | {sum(c)} |")
# alt tip x yıl x alan
alts=sorted({r["alt_tip"] for r in rows}, key=lambda s:(list(AN).index(s[0]) if s[0] in AN else 99, s))
P("\n## Alt tip × yıl ve alan\n\n| Alt tip | "+" | ".join(ys)+" | Top | GM | SAİR | TARİFE | HESAP | 24-25 |\n|---|"+"---|"*(len(ys)+6))
for a in alts:
    c=[sum(1 for r in rows if r["alt_tip"]==a and r["yil"]==y) for y in ys]
    al=[sum(1 for r in rows if r["alt_tip"]==a and r["alan"].startswith(x)) for x in ["GM","SA","TA","HE"]]
    rec=sum(1 for r in rows if r["alt_tip"]==a and r["yil"] in ("2024","2025"))
    P(f"| {a} | "+" | ".join(map(str,c))+f" | {sum(c)} | "+" | ".join(map(str,al))+f" | {rec} |")
# alan bazında alt tip yüzdeleri
P("\n## Alan içinde alt tip payı (%; 5 yıl / 2024-25)\n")
for alan in ["GM","SAİR","TARİFE","HESAP"]:
    sub=[r for r in rows if r["alan"]==alan]; rec=[r for r in sub if r["yil"] in ("2024","2025")]
    if not sub: continue
    cc=collections.Counter(r["alt_tip"] for r in sub); rc=collections.Counter(r["alt_tip"] for r in rec)
    P(f"**{alan}** ({len(sub)} soru): "+" · ".join(f"{k} %{100*v/len(sub):.0f}/{(100*rc[k]/len(rec)) if rec else 0:.0f}" for k,v in cc.most_common()))
    P("")
# alt tip detay
P("\n## Alt tip ayrıntıları\n")
flags=["F_MATRIS","F_MUTLAK","F_TUZAKVERI","F_TUMU","F_YALNIZ","F_DAYANAK","F_MADDENO","F_SERI","F_GUNCEL"]
for a in alts:
    sub=[r for r in rows if r["alt_tip"]==a]
    n=len(sub)
    harf=collections.Counter(r["dogru_harf"][:1] for r in sub)
    uz=collections.Counter(r["dogru_uzunluk"] for r in sub if r["dogru_uzunluk"] not in ("","-"))
    st=collections.Counter(r["sik_turu"] for r in sub)
    fl={f:sum(1 for r in sub if r.get(f,"0") in ("1","1.0","E","evet")) for f in flags}
    on=collections.Counter(r["oncul_sayisi"] for r in sub if r["oncul_sayisi"])
    yk=collections.Counter(r["kok_yuklem"].lower().rstrip("?").strip() for r in sub)
    P(f"### {a} — {n} soru")
    P(f"- Harf: "+", ".join(f"{k}{v}" for k,v in sorted(harf.items())))
    if uz: P(f"- Doğru şık uzunluğu: "+", ".join(f"{k} {v}" for k,v in uz.most_common()))
    P(f"- Şık türü: "+", ".join(f"{k} {v}" for k,v in st.most_common()))
    if on: P(f"- Öncül sayısı: "+", ".join(f"{k}:{v}" for k,v in sorted(on.items())))
    P(f"- Bayraklar: "+", ".join(f"{k[2:]} {v}" for k,v in fl.items() if v))
    P(f"- Yüklemler: "+" | ".join(f"{k} ({v})" for k,v in yk.most_common(8)))
    P(f"- Kurulum örnekleri: "+" | ".join(r["cevap_kurulumu"] for r in sub[:0]))
    for r in sub[:40]:
        P(f"  - {r['yil'][2:]}/{r['no']} [{r['alan']}] {r['kok_ozet'][:130]} → {r['dogru_harf']} · {r['cevap_kurulumu'][:110]}")
    P("")
# bayrak x yıl
P("## Bayrak × yıl\n\n| Bayrak | "+" | ".join(ys)+" | Top |\n|---|"+"---|"*(len(ys)+1))
for f in flags:
    c=[sum(1 for r in rows if r["yil"]==y and r.get(f,"0") in ("1","1.0")) for y in ys]
    P(f"| {f} | "+" | ".join(map(str,c))+f" | {sum(c)} |")
# uzunluk genel, olumlu/olumsuz
P("\n## Doğru şık uzunluğu (cümle/eşleşme şıklı sorular)\n")
for grp,codes in [("Olumsuz (O2, O3, Ö2, E1-yanlış)",["O2","O3"]),("Doğru (G1-G4)",["G1","G2","G3","G4"]),("Tümü",None)]:
    sub=[r for r in rows if r["dogru_uzunluk"] not in ("","-") and (codes is None or r["alt_tip"] in codes)]
    c=collections.Counter(r["dogru_uzunluk"] for r in sub)
    P(f"- {grp}: n={len(sub)} · "+", ".join(f"{k} %{100*v/len(sub):.0f}" for k,v in c.most_common()) if sub else f"- {grp}: -")
open(f"{T}/TOPLU-SAYIMLAR.md","w",encoding="utf-8").write("\n".join(out))
print("\n".join(out[:60]))
