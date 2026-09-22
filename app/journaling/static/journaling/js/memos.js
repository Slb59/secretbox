(function () {
    "use strict";

    const {
        apiUrl,
        updateUrl,
        editUrlTemplate,
        deleteUrlTemplate,
        startDayUrl,
        csrfToken,
    } = window.memosConfig;

    let table = null;

    // ============================================================
    // Fonctions utilitaires
    // ============================================================

    function pkReplace(template, pk){
        return template.replace(/0(?![0-9])/g, pk);
    }

    function getLocalDate() {
        const now = new Date();
        const localDate = new Date(
            now.getTime() - now.getTimezoneOffset() * 60000
        );

        return localDate.toISOString().split("T")[0];
    }

    function getUniqueValues(data, field) {
        return [...new Set(
            data
                .map(row => row[field])
                .filter(value => value !== null && value !== undefined && value !== "")
        )].sort();
    }

    // ============================================================
    // Configuration des colonnes Tabulator
    // ============================================================

    function getColumns(){
        return [
            {   title:"État", 
                field:"state", headerFilter:"list", 
                headerFilterParams:{values:{}}, 
                editor:"list", 
                editorParams:{values:{}}
            },
            {   title:"Durée", 
                field:"duration", 
                hozAlign:"center", 
                headerFilter:true, 
                editor:"input",
                mutatorEdit:function(value){ return Number(value) || 0; },
                sorter:function(a, b){
                    const av = Number(a) || 0;
                    const bv = Number(b) || 0;
                    return av - bv;
                },
                formatter:function(cell){
                    const val = Number(cell.getValue());
                    return Number.isFinite(val) ? val : 0;
                }
            },
            {   title:"Description", 
                field:"description",
                headerFilter:"input", 
                headerFilterPlaceholder:"Filtrer...", 
                width:400,
                editor:"input",
                formatter:function(cell){
                    const val = cell.getValue();
                    if(!val) return "";
                    const lines = val.split("\n");
                    if(lines.length > 3){
                        return lines.slice(0,3).join("<br>") + "<br>...";
                    }
                    return val.replace(/\n/g, "<br>");
                }                    
            },
            {
                title:"Event", 
                field:"event_type", headerFilter:"list", 
                headerFilterParams:{values:{}}, 
                editor:"list", 
                editorParams:{values:{}}
            },
            {
                title:"Catégorie", field:"category", 
                headerFilter:"list", headerFilterParams:{values:{}}, 
                editor:"list", editorParams:{values:{}}
            },
            {
                title:"Qui", field:"who", headerFilter:"input", 
                editor:"input"
            },
            {
                title:"Lieu", field:"place", headerFilter:"list", 
                headerFilterParams:{values:{}}, 
                editor:"list", editorParams:{values:{}}
            },
            {
                title:"Int/Ext", field:"location_type", 
                headerFilter:"list", headerFilterParams:{values:{}}, 
                editor:"list", editorParams:{values:{}}
            },
            {
                title:"Fréquence", field:"periodic", headerFilter:"list", 
                headerFilterParams:{values:{}}, editor:"list", 
                editorParams:{values:{}}
            },
            {
                title:"Priorité", field:"priority", 
                headerFilter:"list", headerFilterParams:{values:{}}, 
                editor:"list", editorParams:{values:{}},
            },
            {
                title:"Today", 
                field:"process_today",
                hozAlign:"center",
                formatter:"tickCross",
                editor:true,
                headerFilter:"select",
                headerFilterParams:{values:{
                    "":"Tous",
                    "true":"Aujourd'hui",
                    "false":"Pas aujourd'hui"}},
                headerFilterFunc:function(headerValue, rowValue, rowData){
                    if(!headerValue) return true;
                    if(headerValue === "true") return !!rowValue;
                    if(headerValue === "false") return !rowValue;
                    return true;
                }
            },
            {   title:"Planifié", 
                field:"planned_date", 
                headerFilter:"date", 
                editor:"date",
                sorter:"date",
                formatter:function(cell){
                    const val = cell.getValue();
                    if(!val) return "";
                    const d = new Date(val);
                    return d.toLocaleDateString("fr-FR");
                }
            },
            {
                title:"Fait", field:"done_date", headerFilter:true, 
                editor:"date", 
                formatter:function(cell){
                const val = cell.getValue();
                if(!val) return "";
                const d = new Date(val);
                return d.toLocaleDateString("fr-FR");
                }
            },
            {
                title:"Note", field:"note", headerFilter:"input", 
                editor:"textarea", width:200
            },
            {
                title:"Actions", field:"pk", hozAlign:"center", 
                formatter:function(cell, formatterParams){
                const pk = cell.getValue();
                const edit = pkReplace(editUrlTemplate, pk);
                const del = pkReplace(deleteUrlTemplate, pk);
                return `<a href="${edit}" class="px-2 py-1 bg-amber-200 rounded mr-1">Éditer</a>` +
                        `<form method="post" action="${del}" style="display:inline;" onsubmit="return confirm('Supprimer ?');">` +
                        `<input type=hidden name=csrfmiddlewaretoken value="{{ csrf_token }}">` +
                        `<button type="submit" class="px-2 py-1 bg-rose-200 rounded">Suppr</button></form>`;
                }
            }
        ]
    }

    
    // ============================================================
    // Création de la table
    // ============================================================
    
    function createTable() {
        table = new Tabulator("#memos-table", {
            placeholder: "Aucune donnée",
            pagination: "local",
            paginationSize: 25,
            columns: getColumns(),
        });

        table.on("cellEditing", function(cell) {
            console.log("EDITING", cell.getField());
        });

        table.on("cellEdited", handleCellEdited);

        table.on("cellEditCancelled", function(cell) {
            console.log("CANCELLED", cell.getField());
        });

        return table;
    }



    // ============================================================
    // Chargement des données
    // ============================================================

// 


            // Ensure process_today field exists and is boolean on all rows
   /*         if (data && data.length) {
                const processValues = [...new Set(data.map(row => !!row.process_today))];
                if(table.getColumn("process_today")){
                    table.getColumn("process_today").updateDefinition({
                        headerFilterParams: {values: {"":"Tous","true":"Aujourd'hui","false":"Pas aujourd'hui"}}
                    });
                }
            }

            // apply URL-based filters to Tabulator (for persistence)
            const params = new URLSearchParams(window.location.search);
            const keys = ["description","who","place","category","state","priority"];
            let hasStateParam = false;
            let hasPriorityParam = false;
            keys.forEach(k => {
                const v = params.get(k);
                if(v){
                    if(k === "state") hasStateParam = true;
                    if(k === "priority") hasPriorityParam = true;
                    table.addFilter(k,"like",v);
                }
            });

            // Set initial state filter via header filter if no state param in URL
            if(!hasStateParam){
                table.setHeaderFilterValue("state", "À faire");
            }
            // Set initial priority filter via header filter if no priority param in URL
            if(!hasPriorityParam){
                table.setHeaderFilterValue("priority", "1-Le matin");
            }
            // set initial planned_date filter via header filter to the minimum date in the data if no planned_date param in URL
            if(!params.get("planned_date")){
                const validDates = data
                    .filter(row => row.state === "À faire")
                    .map(row => row.planned_date)
                    .filter(d => d);
                if(validDates.length > 0){
                    const minDate = new Date(Math.min(...validDates.map(d => new Date(d))));
                    table.setHeaderFilterValue("planned_date", minDate.toISOString().split('T')[0]);
                }
            }
        });

*/

    async function loadMemos() {
        // fetch data including any current query params so server-side filters apply

        try {
            const response = await fetch(
                apiUrl + window.location.search
            );

            if (!response.ok) {
                throw new Error(
                    `Erreur HTTP ${response.status}`
                );
            }

            const data = await response.json();

            const normalizedData = data
                .map(normalizeRow)
                .sort(sortByDuration);

            table.setData(normalizedData);
            table.clearSort(); 
            table.setSort([
                { column: "duration", dir: "asc" }
            ]);
    
                     

            configureFilters(data);
            applyUrlFilters();

        } catch (error) {
            console.error(
                "Erreur lors du chargement des mémos :",
                error
            );
        }
    }

    // ============================================================
    // Normalisation / préparation des données
    // ============================================================
    function normalizeRow(row) {
        return {
            ...row,
            duration: Number(row.duration) || 0,
            process_today: Boolean(row.process_today),
        };
    }

    function sortByDuration(a, b) {
        return a.duration - b.duration;
    }

    // ============================================================
    // Configuration des filtres
    // ============================================================

    function configureFilters(data) {
        configureListFilter("state", data);
        configureListFilter("priority", data);
        configureListFilter("event_type", data);
        configureListFilter("category", data);
        configureListFilter("place", data);
        configureListFilter("periodic", data);

        configureLocationTypeFilter(data);
    }


    function configureListFilter(field, data) {
        const values = getUniqueValues(data, field);

        table.getColumn(field).updateDefinition({
            headerFilterParams: {
                values: values
            },
            editorParams: {
                values: values
            }
        });
    }

    function configureLocationTypeFilter(data) {
        // traitement spécifique des choices Django
        const locationTypeValues = {};
        const locationTypeChoices = data[0]?.location_type_choices || [];
        locationTypeChoices.forEach(choice => {
            locationTypeValues[choice.label] = choice.label;
        });
        table.getColumn("location_type").updateDefinition({
            headerFilterParams: {values: locationTypeValues},
            editorParams: {values: locationTypeValues}
        });
    }

    // ============================================================
    // 9. Édition d'une cellule
    // ============================================================

    function handleCellEdited(cell) {
        console.log("EDITED", cell.getField(), cell.getValue());
        saveCell(cell);
    }

    async function saveCell(cell) {
        const row = cell.getRow().getData();

        const payload = {
            pk: row.pk,
            [cell.getField()]: cell.getValue(),
        };

        try {
            const response = await fetch(updateUrl, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify(payload),
            });


            if (!response.ok) {
                throw new Error(
                    `Erreur HTTP ${response.status}`
                );
            }

            const data = await response.json();

            if (!data.success) {
                throw new Error(
                    data.error || "Erreur inconnue"
                );
            }

        } catch (error) {
            console.error(
                "Erreur lors de la sauvegarde :",
                error
            );

            alert(
                "Erreur lors de la sauvegarde : "
                + error.message
            );
        }
    }

    // ============================================================
    // Démarrage de la journée
    // ============================================================

    function initializeStartDay() {
        const modal = document.getElementById("start-day-modal");
        const dateInput = document.getElementById("start-day-date");
        const confirmButton = document.getElementById("start-day-confirm");
        const cancelButton = document.getElementById("start-day-cancel");
        const startButton = document.getElementById("start-day");

        if (!startButton) {
            return;
        }

        startButton.addEventListener("click", () => {
            dateInput.value = getLocalDate();
            modal?.classList.remove("hidden");
        });


        cancelButton?.addEventListener("click", () => {
            modal?.classList.add("hidden");
        });

        confirmButton?.addEventListener("click", () => {
            startDay(dateInput.value);
        });
    }

    async function startDay(date) {
        const payload = new FormData();
            const fallbackDate = (() => {
                const now = new Date();
                const localDate = new Date(now.getTime() - (now.getTimezoneOffset() * 60000));
                return localDate.toISOString().split('T')[0];
            })();
            payload.append("planned_date", startDayDateInput ? startDayDateInput.value : fallbackDate);

            fetch("{% url 'journaling:start_day' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: payload
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    throw new Error(data.error || "Erreur inconnue");
                }
                if (startDayModal) {
                    startDayModal.classList.add("hidden");
                }
                location.reload();
            })
            .catch(err => {
                alert("Erreur lors du démarrage de la journée: " + err.message);
            });

    }
   

    function setColumnValues(data, field) {
        const values = [
            ...new Set(
                data
                    .map(row => row[field])
                    .filter(value => value)
            )
        ].sort();

        table.getColumn(field).updateDefinition({
            headerFilterParams: { values },
            editorParams: { values },
        });
    }

    
    // ============================================================
    // Ajout d'un mémo
    // ============================================================
    
    function initializeAddButton() {
        const addButton = document.getElementById("reactivity-add");

        if (!addButton) {
            return;
        }

        addButton.addEventListener("click", addMemo);
    }

    function addMemo() {
        // Add a new row to the table on button click

        const activeState = table.getHeaderFilterValue ? (table.getHeaderFilterValue("state") || "À faire") : "À faire";
        const activePriority = table.getHeaderFilterValue ? (table.getHeaderFilterValue("priority") || "1-Le matin") : "1-Le matin";
        const activePlannedDate = table.getHeaderFilterValue ? table.getHeaderFilterValue("planned_date") : "";

        const newRow = {
            state: activeState,
            duration: 10,
            description: "Nouvelle tâche",
            event_type: "",
            category: "Organisation",
            who: "slb",
            place: "partout",
            location_type: "Intérieur",
            periodic: "01-une seule fois",
            planned_date: activePlannedDate,
            priority: activePriority,
            process_today: false,
            done_date: "",
            note: ""
        };

        table.addRow(newRow);
    }
    
    // ============================================================
    // Filtres provenant de l'URL
    // ============================================================
    
    function applyUrlFilters() {
        const params = new URLSearchParams(
            window.location.search
        );

        const fields = [
            "description",
            "who",
            "place",
            "location_type",
            "category",
            "state",
            "priority",
        ];

        fields.forEach(field => {
            const value = params.get(field);

            if (value) {
                table.addFilter(
                    field,
                    "like",
                    value
                );
            }
        });
    }

    function updateUrlParam(key, value){
        const params = new URLSearchParams(window.location.search);
        if(value){ params.set(key, value); }
        else{ params.delete(key); }
        const newUrl = window.location.pathname + '?' + params.toString();
        history.replaceState(null, '', newUrl);
    }

    // ============================================================
    // Initialisation
    // ============================================================

    function init() {
        console.log("initialisation du tableau")
        createTable();
        initializeStartDay();
        initializeAddButton();
        loadMemos();
    }

    init();

})();