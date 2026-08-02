# Otomatik Model Hata Özeti

Bu rapor, yanlış tahmin CSV dosyalarından otomatik olarak oluşturulmuştur.

## validation_matched

Toplam yanlış tahmin sayısı: `2495`

En sık hata: `NEUTRAL → CONTRADICTION`

Bu hatanın sayısı: `587`

### Hata Geçişleri

| Gerçek Sınıf | Tahmin Edilen Sınıf | Sayı |
|---|---|---:|
| NEUTRAL | CONTRADICTION | 587 |
| CONTRADICTION | NEUTRAL | 439 |
| ENTAILMENT | NEUTRAL | 430 |
| NEUTRAL | ENTAILMENT | 387 |
| CONTRADICTION | ENTAILMENT | 382 |
| ENTAILMENT | CONTRADICTION | 270 |

### En Sık Hatanın Genre Dağılımı

| Genre | Sayı |
|---|---:|
| slate | 143 |
| travel | 136 |
| telephone | 113 |
| government | 98 |
| fiction | 97 |

### Temsilî Yanlış Tahminler

#### Örnek 1

- Genre: `slate`
- Gerçek sınıf: `NEUTRAL`
- Tahmin: `CONTRADICTION`
- Premise: 3) Dare you rise to the occasion, like Raskolnikov, and reject the petty rules that govern lesser men?
- Hypothesis: Would you rise up and defeaat all evil lords in the town?

#### Örnek 2

- Genre: `telephone`
- Gerçek sınıf: `NEUTRAL`
- Tahmin: `CONTRADICTION`
- Premise: oh uh-huh well no they wouldn't would they no
- Hypothesis: No, they wouldn't go there.

#### Örnek 3

- Genre: `telephone`
- Gerçek sınıf: `NEUTRAL`
- Tahmin: `CONTRADICTION`
- Premise: i'm not opposed to it but when its when the time is right it will probably just kind of happen you know
- Hypothesis: I cannot wait for it to happen.

## validation_mismatched

Toplam yanlış tahmin sayısı: `2405`

En sık hata: `CONTRADICTION → NEUTRAL`

Bu hatanın sayısı: `493`

### Hata Geçişleri

| Gerçek Sınıf | Tahmin Edilen Sınıf | Sayı |
|---|---|---:|
| CONTRADICTION | NEUTRAL | 493 |
| NEUTRAL | CONTRADICTION | 491 |
| NEUTRAL | ENTAILMENT | 444 |
| ENTAILMENT | NEUTRAL | 417 |
| CONTRADICTION | ENTAILMENT | 342 |
| ENTAILMENT | CONTRADICTION | 218 |

### En Sık Hatanın Genre Dağılımı

| Genre | Sayı |
|---|---:|
| facetoface | 122 |
| verbatim | 104 |
| oup | 97 |
| nineeleven | 88 |
| letters | 82 |

### Temsilî Yanlış Tahminler

#### Örnek 1

- Genre: `oup`
- Gerçek sınıf: `CONTRADICTION`
- Tahmin: `NEUTRAL`
- Premise: The forecasting challenges retailers confront have been amplified in recent years by product proliferation in almost every category.
- Hypothesis: Forecasting has been easier recently due to the updated process we have today.

#### Örnek 2

- Genre: `nineeleven`
- Gerçek sınıf: `CONTRADICTION`
- Tahmin: `NEUTRAL`
- Premise: The hijackers had planned to take flights scheduled to depart at 7:45 (American 11), 8:00 (United 175 and United 93), and 8:10 (American 77).
- Hypothesis: The hijackers planned to take late flights because fewer people would be on board.

#### Örnek 3

- Genre: `verbatim`
- Gerçek sınıf: `CONTRADICTION`
- Tahmin: `NEUTRAL`
- Premise: According to Campbell, the only godlike female figure in the Bible is the Virgin Mary, and she appears, identified as virgin, only in the Gospel according to Luke.
- Hypothesis: There were lots of god like females in the bible, titled goddesses.

## Genel Sonuç

İki validation veri setindeki toplam yanlış tahmin sayısı: `4900`

Hata dağılımları ve temsilî örnekler otomatik olarak raporlanmıştır.
