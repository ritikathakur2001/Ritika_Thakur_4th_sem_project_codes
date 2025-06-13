#!/usr/bin/python3

import cgi
import pandas as pd
import plotly.express as px
import sys

# Read the TSV file name from command-line argument
# input_file = sys.argv[1]
input_file = "6414464_significantvariants.tsv"

print("Content-Type: text/html\n")
print("""
<html>
<head><title>Analysis Results</title></head>
<body>
    <h1><center>Significant Variant Analysis Results</center></h1>
""")

# Handle form inputs
form = cgi.FieldStorage()
pval_threshold_input = form.getvalue('pval_threshold')
ymin_input = form.getvalue('y_min')
ymax_input = form.getvalue('y_max')

# Default values
try:
    pval_threshold = float(pval_threshold_input) if pval_threshold_input else 0.05
except ValueError:
    pval_threshold = 0.05

try:
    y_min = float(ymin_input) if ymin_input else -0.01
except ValueError:
    y_min = -0.01

try:
    y_max = float(ymax_input) if ymax_input else 0.05
except ValueError:
    y_max = 0.05

# Display form
print(f"""
<form method="post">
    <label for="pval_threshold">P-value threshold (e.g., 0.01): </label>
    <input type="text" name="pval_threshold" value="{pval_threshold}">
    <br><label for="y_min">Y-axis min (e.g., -0.01): </label>
    <input type="text" name="y_min" value="{y_min}">
    <br><label for="y_max">Y-axis max (e.g., 0.05): </label>
    <input type="text" name="y_max" value="{y_max}">
    <br><input type="submit" value="Apply Filter">
</form><br>
""")

# If input file is given
if input_file:
    try:
        df = pd.read_csv(input_file, sep="\t")

        column_map = {
            "Block No.([]- overlapping blocks)": "Block No.",
            "Variant (name of the motif)": "Variant",
            "P-value(significance of over-representation of the variant within the block: observed vs. expected by randomness)": "P-Value",
            "Total count of the variants within the positive block across SSs": "Variant Count",
            "Mean position (SD from mean position)": "Mean Position",
            "Position range across SSs within the block": "Position Range"
        }

        for col in df.columns:
            for key in column_map:
                if key in col:
                    df = df.rename(columns={col: column_map[key]})

        if "P-Value" not in df.columns:
            for col in df.columns:
                if "P-value" in col or "p-value" in col:
                    df = df.rename(columns={col: "P-Value"})
                    break

        df["Original P-Value"] = df["P-Value"].astype(str)
        df["P-Value"] = df["P-Value"].astype(str).str.replace(r"<\s*(\d+e-\d+)", r"\1", regex=True)
        df["P-Value"] = df["P-Value"].replace({"< 1e-9": "1e-9"})
        df["P-Value"] = pd.to_numeric(df["P-Value"], errors="coerce")

        if "Mean Position" in df.columns:
            df["Mean Position"] = df["Mean Position"].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)

        df["Variant Name"] = df["Variant"].str.extract(r'(^[^\(]+)')
        df["Variant Type"] = df["Variant"].str.extract(r'(\(.*\))')
        df["Variant Display"] = "<b>" + df["Variant Name"] + "</b><br><b>" + df["Variant Type"].fillna('') + "</b>"

        df_filtered = df[df["P-Value"] <= pval_threshold]

        if df_filtered.empty:
            print(f"<p style='color:orange'>No variants found with P-value ≤ {pval_threshold}</p>")
        else:
            BLOCK_SIZE = 250
            X_AXIS_TICK_INTERVAL = 250
            min_x = 0
            max_x = int(df_filtered["Mean Position"].max()) + BLOCK_SIZE
            x_ticks = list(range(min_x, max_x + 1, X_AXIS_TICK_INTERVAL))

            shapes = []
            for i, start in enumerate(range(min_x, max_x, BLOCK_SIZE)):
                color = "lightgrey" if (i // (BLOCK_SIZE/X_AXIS_TICK_INTERVAL)) % 2 == 0 else "grey"
                shapes.append(dict(
                    type="rect",
                    x0=start,
                    x1=start + BLOCK_SIZE,
                    y0=y_min,
                    y1=y_max,
                    fillcolor=color,
                    opacity=0.2,
                    line_width=0,
                    layer="below"
                ))

            df_plot = df_filtered.drop(columns=["Original P-Value", "Variant", "Variant Name", "Variant Type"])

            fig = px.scatter(
                df_plot,
                x="Mean Position",
                y="P-Value",
                color="Variant Display",
                size="Variant Count",
                hover_data={
                    "Block No.": True,
                    "Position Range": True,
                    "Variant Count": True,
                    "P-Value": ":.10f",
                    "Variant Display": True
                },
                labels={
                    "Mean Position": "Mean Position (bp)",
                    "P-Value": "P-Value",
                    "Variant Count": "Variant Count"
                },
                title=f"Over-representation of Variants (P ≤ {pval_threshold})",
                template="plotly_white"
            )

            fig.update_yaxes(range=[y_min, y_max])
            fig.update_layout(
                shapes=shapes,
                xaxis=dict(tickvals=x_ticks, title="Mean Position (bp)"),
                yaxis=dict(title="P-Value"),
                legend_title_text="Variants"
            )

            fig.for_each_trace(lambda trace: trace.update(
                hovertemplate=trace.hovertemplate.replace("Variant Display=", "")
            ))

            print(fig.to_html(full_html=False, include_plotlyjs='cdn'))

    except Exception as e:
        print(f"<p style='color:red'>Error processing file: {str(e)}</p>")
else:
    print("<p>No file uploaded</p>")

print("</body></html>")


