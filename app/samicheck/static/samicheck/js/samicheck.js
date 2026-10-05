(function () {

    // ============================================================
    // Configuration des colonnes Tabulator
    // ============================================================

    function getColumns(){
        return [
            {
                title: "Date",
                field: "date",
                headerFilter: "date",
                headerFilterParams: {},
                editor: "date",
                editorParams: {},
            },
            {
                title:"Poids",
                field: "weight",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 0.1 },
                editor: "number",
                editorParams: { min: 0, step: 0.1 },
            },
            {
                title:"Heure du coucher",
                field: "bedtime",
                headerFilter: "input",
                headerFilterParams: {},
                editor: "time",
                editorParams: {},
            },
            {
                title:"Heure du réveil",
                field: "wake_time",
                headerFilter: "input",
                headerFilterParams: {},
                editor: "time",
                editorParams: {},
            },
            {
                title:"Temps non stop",
                field: "uninterrupted_sleep",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Forme",
                field: "fitness",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Sieste",
                field: "nap",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Téléphone",
                field: "phone",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Lecture",
                field: "reading",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Total S",
                field: "total_s",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Fruits",
                field: "fruits",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Légumes",
                field: "vegetables",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Plats",
                field: "meals",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Desserts",
                field: "desserts",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Boissons sucrées",
                field: "sugary_drinks",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Boissons non sucrées",
                field: "unsweetened_drinks",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Total A",
                field: "total_a",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Ménage",
                field: "housework",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Jardin",
                field: "garden",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Temps dehors",
                field: "outdoor_time",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Natation-course-vélo",
                field: "swimming_running_cycling",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Yoga-musculation",
                field: "yoga_strength_training",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Total M",
                field: "total_m",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Jeux video",
                field: "video_games",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Jeux PnP",
                field: "board_games",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Administratif",
                field: "administrative",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Informatique",
                field: "computing",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Youtube",
                field: "youtube",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Total I",
                field: "total_i",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            },
            {
                title:"Total SAMI",
                field: "total_sami",
                headerFilter: "number",
                headerFilterParams: { min: 0, step: 1 },
                editor: "number",
                editorParams: { min: 0, step: 1 },
            }
        ]}
    
    // ============================================================
    // Création de la table
    // ============================================================
    function createTable() {
        const indicatorColumns = JSON.parse(
            document.getElementById("samicheck-columns").textContent
        );
        const data = JSON.parse(
            document.getElementById("samicheck-data").textContent
        );

        table = new Tabulator("#samicheck-table", {
            placeholder: "Aucune donnée",
            pagination: "local",
            paginationSize: 25,
            layout: "fitData",
            data,
            columns: [
                {
                    title: "Date",
                    field: "date",
                    headerFilter: "input",
                    sorter: "date",
                },
                ...indicatorColumns.map(column => ({
                    ...column,
                    hozAlign: "center",
                    headerFilter: "number",
                    sorter: "number",
                })),
            ],
        });

        return table;
    }

    // ============================================================
    // Édition d'une cellule
    // ============================================================
    function handleCellEdited(cell) {
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
    // Chargement des données
    // ============================================================
    async function loadData() {
        // fetch data including any current query params 
        // so server-side filters apply

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
            
            table.setData(normalizedData);
            table.clearSort(); 

        } catch (error) {
            console.error("Erreur lors du chargement des données :", error);
        }
    }

    // ============================================================
    // Normalisation / préparation des données
    // ============================================================
    function normalizeRow(row) {
        return {
            ...row,
        };
    }


    // ============================================================
    // Initialisation
    // ============================================================
    function init() {
        createTable();
    }

    init();

})();