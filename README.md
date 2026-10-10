# Kepler TCE Clustering and Anomaly Analysis

Exploratory unsupervised analysis of 34,032 threshold-crossing events (TCEs) from the NASA Kepler Q1-Q17 DR25 table. The notebook applies KMeans, DBSCAN, Isolation Forest and PCA to four signal features and reports what each method finds.

A TCE is a transit-like signal flagged by the Kepler pipeline. TCEs are candidate signals, not confirmed planets.

**Notebook:** `nasa_exoplanet_pattern_mining.ipynb`

---

## Data

**Source:** NASA Exoplanet Archive, Kepler Q1-Q17 DR25 TCE table (`q1_q17_dr25_tce`)

- 34,032 rows and 113 columns in the raw file
- Dropped four identifier and link columns: `rowid`, `tce_delivname`, `tce_datalink_dvs`, `tce_datalink_dvr`
- Dropped all columns that were 100% missing
- 93 numerical columns remained

## Features used in the models

| Feature | Description | Median | Max |
|---------|-------------|--------|-----|
| `tce_period` | Orbital period (days) | 27.3 | 726.7 |
| `tce_depth` | Transit depth (ppm) | 336 | 1,204,000 |
| `tce_duration` | Transit duration (hours) | 5.0 | 237.4 |
| `tce_model_snr` | Model signal-to-noise ratio | 8.7 | 50,830 |

All four features are strongly right-skewed. They were standardized with `StandardScaler` before modeling.

Log-transformed versions of depth, SNR and period were created. Only log depth was plotted (histogram); the models use the standardized raw features. Applying `log1p` to SNR raised a divide-by-zero warning because the table's minimum SNR is -1.

---

## Methods

| Method | Settings |
|--------|----------|
| KMeans | k = 4, `random_state=42` |
| Silhouette score | computed on the KMeans labels |
| DBSCAN | `eps=0.8`, `min_samples=10` |
| Isolation Forest | `contamination=0.05`, `random_state=42` |
| PCA | 2 components, used for visualization |
| Random Forest | 200 trees, trained to predict the KMeans labels |
| Welch's t-test | transit depth, high-SNR vs low-SNR (split at median SNR) |

---

## Results

### KMeans (k = 4)

Silhouette score: **0.56**

| Cluster | Mean period (d) | Mean depth (ppm) | Mean duration (h) | Mean SNR |
|---------|----------------|------------------|-------------------|----------|
| 0 | 397.9 | 2,077 | 13.9 | 13.8 |
| 1 | 9.4 | 182,399 | 5.8 | 10,761 |
| 2 | 31.7 | 3,227 | 5.7 | 86.7 |
| 3 | 36.3 | 308,357 | 6.2 | 1,217 |

Clusters 1 and 3 have very large mean depth and SNR. Cluster 0 has the longest mean period.

### DBSCAN

`eps=0.8`, `min_samples=10`. The notebook prints 3 distinct labels, a count that includes the noise label (-1) if any points were labeled noise.

### Isolation Forest

`contamination=0.05` flagged **1,702** of 34,032 signals (5.0%). The flagged fraction is set by this parameter.

| Feature | Flagged: median | Not flagged: median |
|---------|----------------|---------------------|
| Depth (ppm) | 81,240 | 302 |
| SNR | 893 | 8.6 |
| Duration (h) | 6.5 | 5.0 |
| Period (d) | 20.1 | 28.6 |

Flagged signals have much higher depth and SNR on average (mean depth 133,691 ppm vs 1,529 ppm; mean SNR 2,096 vs 25.4).

### Random Forest feature importance (predicting KMeans labels)

| Feature | Importance |
|---------|-----------|
| `tce_period` | 0.74 |
| `tce_duration` | 0.12 |
| `tce_depth` | 0.10 |
| `tce_model_snr` | 0.03 |

### Welch's t-test: depth in high-SNR vs low-SNR signals

t = 2.60, p = 0.0094. Depth differs between the two groups at the 0.05 level.

---

## Limitations

- The models use four of the 93 numerical columns.
- Clustering and anomaly detection were run on standardized raw features. All four are heavily skewed, so extreme values strongly influence the results.
- The anomaly fraction (5%) is determined by the `contamination` setting.
- The Random Forest predicts labels generated from the same four features, so its importances describe the KMeans partition and not a physical driver.
- No disposition labels (planet candidate vs false positive) are used, so clusters and anomalies are not matched to known signal types.
- Results come from a single run with fixed seeds; stability across seeds and parameters was not tested.

---

## Reproduce

1. Download the Kepler Q1-Q17 DR25 TCE table from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu) as CSV.
2. Set the CSV path in the first cell of the notebook.
3. Install dependencies and run the cells in order:

```
pip install -r requirements.txt
```

Libraries: pandas, NumPy, SciPy, scikit-learn, Matplotlib.

---

## Interactive dashboard

[Live Streamlit dashboard](https://kepler-tce-clustering-anomaly-analysis-v69ajwnosl7nesjkkhuappg.streamlit.app/) (code in `app.py`)

![Dashboard demo 1](demo1.gif)
![Dashboard demo 2](demo2.gif)

---

## Data acknowledgment

This research uses data from the NASA Exoplanet Archive, operated by the California Institute of Technology under contract with NASA through the Exoplanet Exploration Program. This project is not affiliated with or endorsed by NASA.

## Author

Amna Fatima
