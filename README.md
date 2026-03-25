popíšete postup řešení
    přečtení si zadání, cheatsheetů a odkazů, postupně se snažit oskládat kod jak puzzle a částmi razení s ai
odpovíte na otázky ze zadání 
    Které sloupce vypadají problematicky?
        lamp_distance_cm, voltage_v, current_a, temperature_c, timestamp, weather,room, panel_id,   angle_deg, power_w, light_intensity_lux, lamp_distance_cm
    Jaké typy chyb jsi našel?
        špatné typy, překlepy, nekonzistentnost, záporné hodnoty
    Jsou hodnoty stejné? Pokud ne, proč?
        Ne, různé druhy měření
    Jak úhel ovlivňuje výkon?
        Při vyším úhlu výkon klesá
    Dává to fyzikální smysl?
        ano
    Jak silná je závislost?
        0,4
    Je lineární?
        ano
    Kde panel funguje lépe a proč?
        venku na střeše, kvůli světlu
    Jak bys optimalizoval experiment?
        měřit venku za slunečna pod úhlem 10 stupňů
    jsou to chyby, nebo zajímavý jev?
        vevnitř chybné venku jev
stručně porovnáte pandas vs polars (co vám přišlo lepší / horší)
    polars mi dávalo větší smysl, ale spíš protože jsem ho dělala jako druhý, ale pandas zase zvládlo tabulku oddělenou čárkami, polars mělo problém, a také polars mělo v zadání hint takže se lépe hledalo co použít