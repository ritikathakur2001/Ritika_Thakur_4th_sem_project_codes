#!/usr/bin/python3

import cgi
import pandas as pd
import plotly.graph_objects as go
import random
import os
import tempfile
import sys

input_file = sys.argv[1]
# input_file = "69123564_covariants.tsv"


# Function to convert TSV to CSV
def convert_tsv_to_csv(tsv_file):
    csv_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    df = pd.read_csv(tsv_file, sep="\t", skiprows=1)
    df.to_csv(csv_file.name, index=False)
    return csv_file.name

# Output headers for CGI
print("Content-type: text/html\n")
print("<html>")
print("<head><title>Co-variant Analysis of Motifs</title></head>")
print("<body>")
print("<h1>Co-variant Analysis of Motifs</h1>")

# Handle file upload
form = cgi.FieldStorage()
if not input_file:
    print("<p>No file uploaded. Please upload a TSV file.</p>")
else:
    # Convert TSV to CSV
    csv_file_path = convert_tsv_to_csv(input_file)

    # Load the CSV data
    df = pd.read_csv(csv_file_path)

    # Remove extra spaces in column names
    df.columns = df.columns.str.strip()

    # Step 1: Identify the correct P-value column dynamically
    possible_pval_cols = [col for col in df.columns if "P-value" in col]

    if not possible_pval_cols:
        print("<p>Error: P-value column not found!</p>")
    else:
        pval_column = possible_pval_cols[0]
        
        # Processing the DataFrame as per original logic
        df[pval_column] = df[pval_column].astype(str).str.strip()
        df[pval_column] = df[pval_column].replace({"< 1e-9": "1e-9"})
        df[pval_column] = pd.to_numeric(df[pval_column], errors="coerce")

        varA_col = [col for col in df.columns if "VarA Mean Position" in col][0]
        varB_col = [col for col in df.columns if "VarB Mean Position" in col][0]

        df["VarA_Mean"] = df[varA_col].str.extract(r"(\d+)").astype(float)
        df["VarB_Mean"] = df[varB_col].str.extract(r"(\d+)").astype(float)
        df["Variant_Pair"] = df["VarA(Name of the motif)"] + " - " + df["VarB(Name of the motif)"]  # concatenating VarA and VarB together 

        unique_pairs = df["Variant_Pair"].unique()
        color_map = {pair: f"hsl({random.randint(0, 360)}, 100%, 50%)" for pair in unique_pairs} # color of the legend 
        df["Color"] = df["Variant_Pair"].map(color_map)

        # Filter to get only the most significant variants (lowest 100 P-values)
        df = df[(df[pval_column] >= -0.01) & (df[pval_column] <= 0.05)]
        df = df.nsmallest(100, pval_column)  # Select top 100 based on P-value
        
        # Create the plot
        fig = go.Figure()
        for pair in unique_pairs:
            subset = df[df["Variant_Pair"] == pair]

            if subset.empty:
                continue

            # Add traces for Variant I
            fig.add_trace(go.Scatter(
                x=subset["VarA_Mean"],
                y=subset[pval_column],
                mode="markers",
                marker=dict(size=10, color=subset["Color"].iloc[0], opacity=0.7),
                name=f"I ({pair})",  # Changed from "Co-variant A" to "I"
                hovertemplate="<b>I:</b> %{text}<br>" +  # Changed from "Co-variant A" to "I"
                              "<b>P-Value:</b> %{y:.10f}<br>" +
                              "<b>Score:</b> %{customdata[0]:.2f}",
                text=subset["VarA(Name of the motif)"],
                customdata=subset[["VarA_Mean"]].values
            ))

            # Add traces for Variant II
            fig.add_trace(go.Scatter(
                x=subset["VarB_Mean"],
                y=subset[pval_column],
                mode="markers",
                marker=dict(size=10, color=subset["Color"].iloc[0], opacity=0.7),
                name=f"II ({pair})",  # Changed from "Co-variant B" to "II"
                hovertemplate="<b>II:</b> %{text}<br>" +  # Changed from "Co-variant B" to "II"
                              "<b>P-Value:</b> %{y:.10f}<br>" +
                              "<b>Score:</b> %{customdata[0]:.2f}",
                text=subset["VarB(Name of the motif)"],
                customdata=subset[["VarB_Mean"]].values
            ))

        # Add background colors and layout adjustments
        x_min, x_max = df[["VarA_Mean", "VarB_Mean"]].min().min(), df[["VarA_Mean", "VarB_Mean"]].max().max()

        # Ensure the background rectangles start from 0
        for i in range(0, int(x_max) + 250, 250):
            fig.add_shape(
                type="rect",
                x0=i, x1=i + 250, y0=-0.01, y1=0.05,
                fillcolor="lightgrey" if ((i // 250) % 2 == 0) else "grey",
                opacity=0.3,
                layer="below",
                line_width=0
            )

        fig.update_layout(
            title="Co-variant Analysis of Motifs",
            xaxis=dict(title="Mean Position of Co-variant I & II", range=[0, x_max], tickmode="linear", tick0=0, dtick=250),
            yaxis=dict(title="P-Value (Significance)", range=[-0.01, 0.05]),
            hovermode="closest",
            showlegend=True,
            legend_title_text="   Co-variant I and II",  # Set the legend title
            dragmode='zoom'  # Allow dragging to zoom option
        )

        # Show the plot as HTML
        plot_html = fig.to_html(full_html=False)
        print(plot_html)
        
# Final HTML structure
print("</body>")
print("</html>")
