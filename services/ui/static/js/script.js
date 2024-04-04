// Your JSON structure
const jsonData = {
    "delivery_facts": {
        "table": "De 'delivery_facts' tabel bevat geaggregeerde informatie over het aantal pakketen dat elke klant ooit heeft ontvangen.",
        "account_id_hashed": " Deze kolom bevat een unieke identificatiecode voor elk klantaccount. De waarden in deze kolom zijn niet uniek binnen deze tabel, aangezien er meerdere records kunnen zijn voor dezelfde klant. Deze kolom dient als vreemde sleutel die verwijst naar de primaire sleutel in de 'delivery_preference' tabel.",
        "month_id": " Dit veld bevat de maand en het jaar waarin \u00e9\u00e9n of meerdere pakketten aan de klant zijn geleverd, opgeslagen in het formaat 'yyyymm'. Bijvoorbeeld, '202312' staat voor december 2023.",
        "number_of_parcels": " Deze kolom geeft het totale aantal pakketten aan dat aan de klant is geleverd. Het omvat alle pakketten ongeacht de leveringsmethode of het aantal pogingen.",
        "parcels_home_1st": " Dit veld geeft het aantal pakketten aan dat succesvol bij de eerste bezorgpoging aan huis is afgeleverd. Het sluit pakketten uit die zijn afgehaald bij afhaalpunten of die bij latere bezorgpogingen zijn afgeleverd."
    },
    "collo_packages": {
        "table": "De 'collo_packages' tabel bevat informatie over pakketten zijn gelevered, of nog moeten worden geleverd door PostNL. De tabel bevat informatie over de jaren 2023 en 2024. Alle datums en tijdstempels zijn opgeslagen in het volgende formaat = 11/08/2023 en 19",
        "account_id_hashed": " Dit veld bevat een identifier voor de klant of het account waaraan het pakket wordt geleverd. De waarden zijn niet uniek voor deze tabel en kunnen duplicaten bevatten. Dit veld fungeert als een vreemde sleutel die verwijst naar de primaire sleutel van de 'delivery_preference' tabel. Het kan leeg zijn voor pakketten die niet aan een specifiek account zijn gekoppeld.",
        "dn_barcode": " Deze kolom bevat unieke identificatiecodes voor elk pakket. Hoewel de meeste waarden uniek zijn, kunnen er enkele duplicaten voorkomen.",
        "da_datum_voormelding": " Bevat de datum waarop de bestelling oorspronkelijk is geplaatst.",
        "da_datum_acceptatie": " Geeft de datum aan waarop het pakket voor het eerst door PostNL is ontvangen. Als een datumkolom leeg is, wordt de waarde '9999-03-03' gebruikt. Dit betekend dat het pakket nog niet door PostNL is ontvangen maar al wel is aangemeld.",
        "da_tijd_acceptatie": "Bevat de tijdstempel voor het moment waarop het pakket voor het eerst door PostNL is ontvangen. Als deze informatie niet beschikbaar is, wordt 'Nvt' weergegeven. Dit betekend dat het pakket nog niet door PostNL is ontvangen maar al wel is aangemeld.",
        "sa_dag_sortering1": " Deze kolom bevat de datum waarop het proces in het sorteercentrum voor het eerst is gestart.",
        "sa_datum_sortering1": " Indien het sorteercentrumproces doorgaat na middernacht, bevat deze kolom de datum van de volgende dag.",
        "sa_tijd_sortering1": " Bevat een tijdstempel wanneer een pakket in een sorteercentrum is gesorteerd.",
        "sa_datum_distributiecollectie": " Bevat de tijdstempel van wanneer het pakket voor het eerst in het sorteercentrum is gesorteerd.",
        "sa_tijd_distributiecollectie": " Geeft de tijdstempel aan van het moment waarop het pakket het distributiecentrum bereikt.",
        "da_datum_herroutering_voor_up1": "Deze kolom bevat de datum waarop het pakket is omgeleid, meestal vanwege een mislukte eerste afleverpoging.",
        "da_tijd_herroutering_voor_up1": " Bevat de tijdstempel van wanneer het pakket is omgeleid.",
        "da_datum_eindstatus": " Geeft de datum aan waarop het pakket uiteindelijk door de klant is ontvangen. Wanneer het pakket nog door de klant is ontvangen bevat de kolom de waarde '9999-03-03'.",
        "da_tijd_eindstatus": "Bevat de tijdstempel voor het moment waarop het pakket door de klant is ontvangen.",
        "ma_gewicht, ma_breedte, ma_lengte, ma_hoogte, ma_volume": " Deze velden bevatten respectievelijk het gewicht, de breedte, lengte, hoogte en het volume van een pakket. Alle waarden zijn gehele getallen. Deze velden kunnen optioneel leeg zijn.",
        "PC4_gea": " Bevat de eerste vier cijfers van de postcode van de klant. Dit zijn de cijfers voorafgaand aan de twee letters in een typische Nederlandse postcode.",
        "da_landcode_gea": " Geeft de landcode van de klant aan. Voor deze dataset bevat het enkel 'NL' voor Nederland.",
        "da_resultaatgroepcode": " Bevat de uiteindelijke status van de levering. Mogelijke opties zijn",
        "da_resultaatcode": " Bevat de uiteindelijke status van het pakket. Mogelijke opties zijn",
        "da_type_adres_gea": " Bevat informatie over of het adres priv\u00e9, particulier of gemengd is.",
        "da_waarnemingsequence": " Het proces pad van een pakket van begin tot eind. Bevat een reeks interne codes die elk een status voorstellen in process."
    },
    "delivery_preference": {
        "table": "De tabel 'delivery_preference' bevat informatie over hoe de klant zijn pakket bij voorkeur geleverd krijgt. In deze tabel staan alleen klanten die een account hebben aangemaakt.",
        "account_id_hashed": " Een unieke waarde voor elke klant/account die geregistreerd is in het systeem. In dit tabel bevat deze kolom geen duplicaten, waardoor deze kolom de primaire sleutel van deze tabel is.",
        "deliverypreference": " Dit veld geeft de voorkeur van de klant aan voor de wijze van pakketlevering. De mogelijke waarden omvatten 'Originele afleverlocatie' (OriginalDeliveryLocation), 'Pakketkluis' (ParcelLocker), 'Openbare pakketkluis' (PublicParcelLocker), 'Winkellocatie' (RetailLocation), en 'Geen' (None). Als dit veld leeg is, betekent dit dat de klant geen voorkeur heeft opgegeven.",
        "datelastupdated": " Dit veld registreert de datum en tijd waarop de leveringsvoorkeur van de klant voor het laatst is bijgewerkt. Het formaat van de datum en tijd is bijvoorbeeld '29/11/2023 15",
        "datecreated": " Dit veld bevat de datum en tijd waarop de record in deze tabel oorspronkelijk is aangemaakt. Het gebruikt hetzelfde datum- en tijdformaat als 'datelastupdated', bijvoorbeeld '29/11/2023 15"
    }
};

function createTableButtons() {
    const container = document.getElementById('tableButtonContainer');
    const tableKeys = Object.keys(jsonData);
    tableKeys.forEach(key => {
        const button = document.createElement('button');
        button.textContent = key;
        button.className = 'button';
        button.onclick = () => createColumnButtons(key);
        container.appendChild(button);
    });
}

function createColumnButtons(parentKey) {
    const container = document.getElementById('columnButtonContainer');
    container.innerHTML = ''; // Clear existing column buttons

    const columnKeys = Object.keys(jsonData[parentKey]);
    columnKeys.forEach(key => {
        const button = document.createElement('button');
        button.textContent = key;
        button.className = 'button';
        button.onclick = () => {
            alert(jsonData[parentKey][key]); // Show the description or handle as needed
        };
        container.appendChild(button);
    });
}

// Initialize table buttons on load
createTableButtons();
