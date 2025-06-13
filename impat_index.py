#!/usr/bin/env python3

import cgitb

print("Content-Type: text/html\n")

cgitb.enable()

print(r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Promoter Analysis</title>
    <style>
        :root {
            /* Define color variables */
            --background: hsl(200, 100%, 5%);
            --foreground: hsl(0, 0%, 98%);
            --card: hsl(200, 70%, 10%);
            --card-foreground: hsl(0, 0%, 98%);
            --primary: hsl(180, 100%, 35%);
            --primary-foreground: hsl(0, 0%, 0%);
            --secondary: hsl(180, 40%, 96%);
            --secondary-foreground: hsl(180, 100%, 20%);
            --muted: hsl(200, 50%, 15%);
            --muted-foreground: hsl(180, 5%, 70%);
            --accent: hsl(164, 100%, 50%);
            --accent-foreground: hsl(0, 0%, 0%);
            --border: hsl(200, 50%, 20%);
            --radius: 0.5rem;
        }

        /* Light theme styles */
        body.light-theme {
            --background: hsl(150, 100%, 95%);
            --foreground: hsl(0, 0%, 20%);
            --card: hsl(150, 70%, 90%);
            --card-foreground: hsl(0, 0%, 20%);
            --primary: hsl(180, 100%, 40%);
            --primary-foreground: hsl(0, 0%, 100%);
            --secondary: hsl(180, 60%, 75%);
            --secondary-foreground: hsl(180, 40%, 20%);
            --muted: hsl(200, 50%, 70%);
            --muted-foreground: hsl(180, 5%, 30%);
            --accent: hsl(164, 100%, 60%);
            --accent-foreground: hsl(0, 0%, 100%);
            --border: hsl(200, 50%, 50%);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, sans-serif;
            background-color: var(--background);
            color: var(--foreground);
            line-height: 1.6;
            min-height: 100vh;
            padding: 2rem;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .card {
            background-color: var(--card);
            border-radius: var(--radius);
            border: 1px solid var(--border);
            padding: 2rem;
            margin-bottom: 2rem;
        }

        h1 {
            text-align: center;
            margin-bottom: 2rem;
            color: var(--card-foreground);
        }

        .theme-toggle {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 1rem;
        }

        .toggle-switch {
            width: 60px;
            height: 30px;
            background-color: var(--primary);
            border-radius: 15px;
            cursor: pointer;
            position: relative;
            transition: background-color 0.3s;
        }

        .toggle-switch::before {
            content: "";
            position: absolute;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            background-color: white;
            top: 2px;
            left: 2px;
            transition: transform 0.3s;
        }

        .toggle-switch.active {
            background-color: var(--accent);
        }

        .toggle-switch.active::before {
            transform: translateX(30px);
        }

        .radio-group {
            margin-bottom: 2rem;
        }

        .radio-label {
            display: block;
            margin-bottom: 1rem;
            cursor: pointer;
            color: var(--card-foreground);
        }

        .input-section {
            display: none;
            margin-top: 1rem;
            padding: 1rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background-color: var(--background);
        }

        .input-section.active {
            display: block;
            animation: fadeIn 0.3s ease-in;
        }

        textarea,
        input,
        select {
            width: 100%;
            padding: 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border);
            border-radius: var(--radius);
            background-color: var(--background);
            color: var(--foreground);
            font-size: 1rem;
        }

        textarea {
            min-height: 150px;
            font-family: monospace;
            resize: vertical;
        }

        select {
            appearance: none;
            padding-right: 2rem;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat;
            background-position: right 0.5rem center;
            background-size: 1.5em;
        }

        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }

        button {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: var(--radius);
            cursor: pointer;
            font-weight: 600;
            transition: opacity 0.2s;
        }

        button:hover {
            opacity: 0.9;
        }

        .btn-primary {
            background-color: var(--accent);
            color: black;
        }

        .btn-outline {
            background-color: transparent;
            border: 1px solid var(--border);
            color: var(--foreground);
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media (max-width: 640px) {
            .button-group {
                flex-direction: column;
            }

            button {
                width: 100%;
            }
        }
    </style>
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .detail-button {
            background-color: #e5e7eb; /* Gray 200 */
            color: #374151; /* Gray 800 */
            padding: 0.5rem 1rem;
            border-radius: 0.375rem; /* Rounded md */
            font-size: 0.875rem; /* text-sm */
            font-weight: 500; /* font-medium */
            cursor: pointer;
            border: 1px solid #d1d5db; /* Gray 300 */
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* shadow-sm */
            transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transition */
        }

        .detail-button:hover {
            background-color: #d1d5db; /* Gray 300 on hover */
            transform: scale(1.05); /* Slightly larger on hover */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a bit more shadow on hover */
        }

        .detail-button:active {
            transform: scale(0.95); /* Slightly smaller on click */
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Reduce shadow on click */
        }

        /* Styles for the table */
        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 2rem;
            border: 1px solid #d1d5db; /* Gray 300 */
            border-radius: 0.5rem;
            overflow: hidden; /* to contain rounded corners of thead and tbody */
        }

        .result-table thead {
            background-color: #f3f4f6; /* Gray 100 */
        }

        .result-table th, .result-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb; /* Gray 200 */
        }

        .result-table th {
            font-weight: 600; /* font-semibold */
            color: #4b5563; /* Gray 700 */
        }

        .result-table tbody tr:last-child td {
            border-bottom: none;
        }

        .result-table .detail-cell {
            text-align: center; /* Center the button in the cell */
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="theme-toggle">
            <div class="toggle-switch" id="themeToggle"></div>
        </div>

        <div class="card">
            <h1>Promoter Analysis and Prediction</h1>

            <form id="analyzeForm">
                <div class="radio-group">
                    <label class="radio-label">
                        <input style="width: 5%" type="radio" name="inputOption" value="fasta" checked />
                        Start with promoter sequence in FASTA format
                    </label>
                    <label class="radio-label">
                        <input  style="width: 5%" type="radio" name="inputOption" value="Gene_ID" />
                        Start with NCBI GENE ID /ENSEMBLE Transcript ID
                    </label>
                    <label class="radio-label">
                        <input style="width: 5%" type="radio" name="inputOption" value="tissue" />
                        Tissue/Condition and Species
                    </label>
                </div>

                <div id="fastaSection" class="input-section active">
                    <p>(Promoter Sequence)</p>
                    <textarea
                        id="sequence"
                        name="sequence"
                        placeholder=">ENSG00000139618
ATGGTCGTACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGA
CTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGA"
                    ></textarea>

                    <button type="button" id="toggleAdvancedBtn">
                        Show Advanced Options
                    </button>

                    <div id="advancedOptions" style="display: none; margin-top: 15px">
                        <p><strong>Advanced Options:</strong></p>

                        <fieldset>
                            <legend>Enter Query Motif(s)</legend>
                            <label>
                                <input
                                    type="text"
                                    name="motif"
                                    size="40"
                                    placeholder="e.g. TATAWAWR, RGWVY"
                                />
                                <a
                                    href="/krishna/motdet_version3/User_guide/h_userguide.htm#input"
                                    class="hintanchor"
                                    onMouseover="showhint('For example: TATAWAWR, RGWVY', this, event, '200px')"
                                >
                                    <img
                                        src="/krishna/motdet_version3/images/Que1_MotDet.png"
                                        width="15"
                                        height="25"
                                        align="absmiddle"
                                    />
                                </a>
                            </label>
                        </fieldset>

                        <fieldset>
                            <legend>Select Known Core Promoter Elements (CPE)</legend>
                            <label
                                ><input type="checkbox" name="query" value="TATAWAWR" />
                                TATA</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="YYANWYY" />
                                INR</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="DSGYGGRASM" />
                                XCPEI</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="RGWYV" /> DPE</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="SSRCGCC" /> BRE<sup
                                    >u</sup
                                ></label
                            >
                            <label
                                ><input type="checkbox" name="query" value="RTDKKKK" /> BRE<sup
                                    >d</sup
                                ></label
                            >
                            <label
                                ><input type="checkbox" name="query" value="CSARCSSAACGS" /> MTE1</label
                            >
							<label
                                ><input type="checkbox" name="query" value="SVAGCSSRGCGS" /> MTE2</label
                            >
                        </fieldset>

                        <fieldset>
                            <legend>Derived Consensus of CPE from JASPAR Matrices</legend>
                            <label
                                ><input type="checkbox" name="query" value="GTATAAAAGGCGGGG" />
                                TATA</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="TCAGTCTT" /> INR</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="GGGCGGGACC" />
                                XCPE1</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="GAAGATGTT" /> DPE</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="AGGGGGCGGGGCTG" /> GC
                                Box</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="ACTAGCCAATCA" />
                                CCAAT-Box</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="TTTCGAGCGGARCGGTCGY" /> MTE</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="AGCGCGCC" /> BRE<sup
                                    >u</sup
                                ></label
                            >
                            <label
                                ><input type="checkbox" name="query" value="GTTTGTT" /> BRE<sup
                                    >d</sup
                                ></label
                            >
                            <label
                                ><input type="checkbox" name="query" value="GCTCCG" />
                                MED-1</label
                            >
                            <label
                                ><input type="checkbox" name="query" value="GCTTCC" /> DCE</label
                            >
                        </fieldset>
                    </div>
                </div>

                <!-- Gene ID Input -->
          <div id="Gene_IDSection" class="input-section" style="display: none">
            <input type="radio" name="idtype" value="gn" style="width:5%" checked>Gene</input>
            <input type="radio" name="idtype" value="tr" style="width:5%">Transcript</input><br>
            <label>Upstream Region</label>
            <input type="text" name="up" value="1000" style="width:10%"></input>
            <label>Downstream Region</label>
            <input type="text" name="down" value="500" style="width:10%"></input>
            <p>(NCBI GENE ID /ENSEMBLE Transcript ID)</p>
                    <textarea
                        id="Gene_ID"
                        name="Gene_ID"
                        placeholder="55174/ENST00000369985"
                    ></textarea>
                    </div>

                <div id="tissueSection" class="input-section" style="display: none">
                    <div>
                        <label>Tissue/Condition:</label>
                        <input
                            type="text"
                            id="tissue"
                            name="tissue"
                            placeholder="Enter tissue or condition"
                        />
                    </div>
                    <div>
                        <label>Species:</label>
                        <select name = "species" id="species">
                            <option value="human">Human</option>
                            <option value="mouse">Mouse</option>
                            <option value="rat">Rat</option>
                        </select>
                    </div>
                </div>

                <div class="button-group">
                    <button type="button" class="btn-outline" id="loadSampleBtn">
                        Load sample info
                    </button>
                    <button type="submit" id="submitButton" class="btn-primary">Submit</button>
                    <button type="button" class="btn-outline" id="resetBtn">
                        Reset
                    </button>
                </div>
            </form>
        </div>
    </div>

    <script>
	
    document.addEventListener('DOMContentLoaded', () => {
        const form = document.getElementById("analyzeForm");
        const radioButtons = form.querySelectorAll('input[name="inputOption"]');
        const fastaSection = document.getElementById("fastaSection");
        const geneIDSection = document.getElementById("Gene_IDSection");
        const tissueSection = document.getElementById("tissueSection");
        const fastaInput = fastaSection.querySelector("textarea");
        const geneIDInput = geneIDSection.querySelector("#Gene_ID");
        const geneIDTypeInput = geneIDSection.querySelector('input[name="idtype"]:checked');
        const tissueInput = document.getElementById("tissue");
        const speciesInput = document.getElementById("species");
        const loadSampleBtn = document.getElementById("loadSampleBtn");
        const resetBtn = document.getElementById("resetBtn");
        const themeToggle = document.getElementById("themeToggle");
        const toggleAdvancedBtn = document.getElementById("toggleAdvancedBtn");
        const advancedOptions = document.getElementById("advancedOptions");
        const submitButton = document.getElementById('submitButton');


        const sampleData = {
            fasta: ">ENSG00000139618\nATGGTCGTACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGA\nCTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGA",
            Gene_ID: "55174/ENST00000369985",
            tissue: "lung/lung cancer",
            species: "human",
        };

        function updateSections(selectedValue) {
            fastaSection.style.display =
                selectedValue === "fasta" ? "block" : "none";
            geneIDSection.style.display =
                selectedValue === "Gene_ID" ? "block" : "none";
            tissueSection.style.display =
                selectedValue === "tissue" ? "block" : "none";
        }

        function getOptionFromURL() {
            const params = new URLSearchParams(window.location.search);
            return params.get("option");
        }

        const optionFromURL = getOptionFromURL();
        if (optionFromURL) {
            const radioToSelect = form.querySelector(
                `input[name="inputOption"][value="${optionFromURL}"]`
            );
            if (radioToSelect) {
                radioToSelect.checked = true;
                updateSections(optionFromURL);
            }
        } else {
            updateSections(
                form.querySelector('input[name="inputOption"]:checked')?.value ||
                    "fasta"
            );
        }

        radioButtons.forEach((radio) => {
            radio.addEventListener("change", function () {
                updateSections(this.value);
            });
        });

        toggleAdvancedBtn.addEventListener("click", function () {
            if (advancedOptions.style.display === "none") {
                advancedOptions.style.display = "block";
                toggleAdvancedBtn.textContent = "Hide Advanced Options";
            } else {
                advancedOptions.style.display = "none";
                toggleAdvancedBtn.textContent = "Show Advanced Options";
            }
        });

        loadSampleBtn.addEventListener("click", function () {
            const selected = form.querySelector(
                'input[name="inputOption"]:checked'
            )?.value;
            if (selected === "fasta") {
                fastaInput.value = sampleData.fasta;
                geneIDInput.value = "";
                tissueInput.value = "";
                speciesInput.value = "";
            } else if (selected === "Gene_ID") {
                geneIDInput.value = sampleData.Gene_ID;
                fastaInput.value = "";
                tissueInput.value = "";
                speciesInput.value = "";
            } else if (selected === "tissue") {
                tissueInput.value = sampleData.tissue;
                speciesInput.value = sampleData.species;
                fastaInput.value = "";
                geneIDInput.value = "";
            }
        });

        resetBtn.addEventListener("click", function () {
            form.reset();
            fastaInput.value = "";
            geneIDInput.value = "";
            tissueInput.value = "";
            speciesInput.value = "";
            updateSections("fasta");
            advancedOptions.style.display = "none";
            toggleAdvancedBtn.textContent = "Show Advanced Options";
        });

    
        form.addEventListener('submit', function(e) {
            //e.preventDefault(); // Prevent the default form submission

            const selected = form.querySelector('input[name="inputOption"]:checked')?.value;
            form.action = "impat_motdet.pl" // Call the function to handle the FASTA submission
            if (selected === 'tissue') {
                //  No need to prevent default here, the original code submits to external site.
                form.action = 'http://resources.ibab.ac.in/cgi-bin/MGEXdb/microarray/scoring/interface/Homepage.pl';
                form.submit();
            }
           
        });

        themeToggle.addEventListener("click", function () {
            document.body.classList.toggle("light-theme");
            themeToggle.classList.toggle("active");
        });
    });
    </script>
</body>
</HTML>
""")
