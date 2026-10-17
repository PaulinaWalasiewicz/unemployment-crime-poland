[English](README.md) | **Polski**

# Bezrobocie a przestępczość w polskich województwach (2014-2024)

Czy w województwach z wyższym bezrobociem jest też więcej przestępstw?
Sprawdziłam to na oficjalnych danych GUS dla wszystkich 16 województw.

**Krótka odpowiedź:** nie. W tych danych wyższe bezrobocie nie idzie w parze z większą przestępczością.
Jest raczej odwrotnie - ale to najpewniej przez inne różnice między regionami,
a nie przez samo bezrobocie.

## Skąd ten projekt

Ten temat zaczął się jako projekt na studiach. W tej wersji chciałam spojrzeć na niego inaczej:
użyłam przestępstw na 1000 mieszkańców zamiast liczby przestępstw, porównywałam województwa w obrębie jednego roku
zamiast w czasie, wybrałam tylko lata z tym samym sposobem liczenia przestępstw, a wszystkie dane pobrałam
przez API BDL zamiast zbierać je z plików Excel ze stron policji i GUS.

## Co odkryłam

**1. Bezrobocie spadło o ponad połowę, a przestępczość została prawie taka sama.**
W latach 2014-2024 bezrobocie w Polsce spadło z 11,4% do 5,1%.
Przestępczość na 1000 mieszkańców przez cały czas wynosiła mniej więcej od 19,5 do 23.

![Przestępczość w Polsce](images/01_crime_poland.png)
![Bezrobocie w Polsce](images/02_unemployment_poland.png)

**2. W województwach z wyższym bezrobociem jest mniej przestępstw, a nie więcej.**
Korelacja między bezrobociem a przestępczością jest ujemna w każdym roku, od -0,32 w 2014 do -0,68 w 2024.
Podkarpackie ma najwyższe bezrobocie i najniższą przestępczość, a Dolnośląskie, Śląskie i Małopolskie
mają niskie bezrobocie i najwięcej przestępstw. Możliwy powód: regiony z dużymi miastami
mają jednocześnie więcej pracy i więcej okazji do przestępstw.

![Bezrobocie a przestępczość](images/04_scatter_2014_2024.png)

**3. Najmocniej widać to przy przestępstwach przeciwko mieniu, przy drogowych prawie wcale.**
Kradzieży i włamań jest więcej tam, gdzie bezrobocie jest niskie.
Przestępstwa drogowe i przeciwko życiu i zdrowiu prawie nie mają związku z bezrobociem.

![Korelacja w kolejnych latach](images/06_correlation_by_year.png)

**4. Zmiany w czasie też się nie pokrywają.**
W województwach, gdzie bezrobocie spadło najbardziej, przestępczość nie spadła bardziej niż w innych (korelacja -0,15).

![Zmiana w ciągu 10 lat](images/08_change_2014_2024.png)

**5. Nietypowe wartości pochodzą z pojedynczych rodzajów przestępstw.**
W Śląskim w 2022 i w Zachodniopomorskim w 2019 były jednoroczne skoki przestępczości - w Śląskim przez przestępstwa gospodarcze,
w Zachodniopomorskim przez przestępstwa kryminalne. Małopolskie to jedyne województwo, w którym przestępczość była wyższa w 2024 niż w 2014.

## Dashboard w Power BI

Interaktywna wersja analizy. Można wybrać rok i kategorię przestępstw,
a wszystkie wykresy się zmieniają: mapa, wykres punktowy (bezrobocie a przestępczość), trend dla Polski i ranking.

![Dashboard](images/dashboard.png)

Plik jest w folderze `dashboard/`.

## Dane

Wszystkie dane pochodzą z [Banku Danych Lokalnych GUS (BDL)](https://bdl.stat.gov.pl/) i zostały pobrane przez API BDL.

| Dane | Lata |
|---|---|
| Stopa bezrobocia | 2014-2024 |
| Liczba ludności | 2014-2024 |
| Przestępstwa - ogółem i 5 kategorii (kryminalne, gospodarcze, przeciwko mieniu, drogowe, przeciwko życiu i zdrowiu), jako liczba przestępstw i na 1000 mieszkańców | 2014-2024 |
| Stopa bezrobocia i przestępczość dla całej Polski (do sprawdzenia moich obliczeń) | 2014-2024 |

Dane są udostępnione na licencji CC BY 4.0.

### Dlaczego tylko 2014-2024?

Sposób liczenia przestępstw przez policję kilka razy się zmieniał, więc starszych i nowszych danych nie da się w pełni porównać:

| Rok | Co się zmieniło |
|---|---|
| 2013 | Nie są już liczone przestępstwa z postępowań prowadzonych przez prokuraturę i inne organy |
| 2014 | Nie są już liczone przestępstwa popełnione przez nieletnich |
| 2025 | Policja zmieniła kategorie przestępstw |

Od 2013 do 2014 przestępczość spadła o 15-22% w większości województw, dużo bardziej niż w innych latach, więc zaczęłam od 2014.
GUS przeliczył też liczbę ludności w 2021 roku, więc wskaźniki przed i po 2020 mogą się trochę różnić.

## Jak to zrobiłam

1. **Pobieranie** (`scripts/fetch_data.py`) - pobiera wszystkie zmienne z API BDL i zapisuje je do `data/raw/`.
2. **Czyszczenie** (`notebooks/01_cleaning.ipynb`) - sprawdza braki danych, wybiera lata, tworzy dwie czyste tabele (bezrobocie i przestępstwa) i porównuje wskaźniki GUS z moimi obliczeniami.
3. **Analiza** (`notebooks/02_analysis.ipynb`) - trendy dla Polski, porównanie województw,
   korelacje dla każdego roku i kategorii, nietypowe wartości i zmiana w ciągu 10 lat.
4. **Dashboard** (`dashboard/`) - raport w Power BI zbudowany na czystych tabelach, ze schematem gwiazdy (tabele województw i lat)
   i miarami DAX, które liczą wskaźniki tak samo jak w notebooku.

Na co musiałam uważać:
- Używam przestępstw **na 1000 mieszkańców**, a nie liczby przestępstw, bo w dużych województwach jest więcej przestępstw po prostu dlatego, że mieszka tam więcej ludzi.
- Porównuję województwa **w obrębie jednego roku**, bo zarówno bezrobocie, jak i przestępczość zmieniały się w czasie, a mieszanie lat mogłoby pokazać związek, który wynika tylko z upływu czasu.
- Kategorie przestępstw **nakładają się** (jedno przestępstwo może być w kilku kategoriach), więc nigdy ich nie sumuję.
- Żeby policzyć wskaźnik dla całego kraju, sumuję wszystkie przestępstwa i wszystkich mieszkańców, zamiast brać średnią ze wskaźników województw.

## Struktura projektu

```
unemployment-crime-poland/
├── data/
│   ├── raw/            # dane pobrane z BDL
│   └── processed/      # czyste tabele używane w analizie
├── scripts/
│   └── fetch_data.py   # pobiera dane z API BDL
├── notebooks/
│   ├── 01_cleaning.ipynb
│   └── 02_analysis.ipynb
├── images/             # wykresy z analizy
└── dashboard/          # dashboard w Power BI
```

## Jak uruchomić

```
pip install -r requirements.txt
python scripts/fetch_data.py
```

Potem otwórz notebooki z folderu `notebooks/` i uruchom je po kolei.

## Narzędzia

Python (pandas, numpy, matplotlib, requests), Jupyter Notebook, API BDL, Power BI