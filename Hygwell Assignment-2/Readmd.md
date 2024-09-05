# Website Traffic Analysis

This project analyzes website traffic data to extract insights regarding pageviews, event distribution, geographical distribution of users, click-through rates (CTR), and correlation between clicks and pageviews.

## Dataset

The dataset contains the following columns:

- `event`: The type of event (e.g., pageview, click, preview, play).
- `date`: The timestamp of the event.
- `country`: The country of the user who generated the event.
- `city`: The city of the user who generated the event.
- `artist`: The artist associated with the event.
- `album`: The album associated with the event.
- `track`: The track associated with the event.
- `isrc`: The ISRC (International Standard Recording Code) of the track.
- `linkid`: The ID of the link associated with the event.

## Analysis Overview

### Total and Daily Pageviews
- **Total Pageviews**: 142,015
- **Average Daily Pageviews**: 20,288

### Event Distribution
The dataset contains multiple types of events. The distribution of events is as follows:

- **Pageviews**: 142,015
- **Clicks**: 55,732
- **Previews**: 28,531

### Geographical Distribution
The top contributing countries for pageviews are:

1. **Saudi Arabia**: 28,873 pageviews
2. **India**: 27,286 pageviews
3. **United States**: 20,839 pageviews
4. **France**: 9,674 pageviews
5. **Iraq**: 4,897 pageviews

The dataset contains users from 211 different countries.

### Click-Through Rate (CTR) Analysis
- **Overall CTR**: 0.39
- **CTR per Link**: The CTR varies for different links, ranging from 0.22 to 1.00.

### Correlation Analysis
Correlation analysis between clicks and pageviews was performed using Pearson and Spearman correlation coefficients:

- **Pearson Correlation**: [Insert calculated value]
- **Spearman Correlation**: [Insert calculated value]

These correlations help to understand the relationship between user engagement (clicks) and visibility (pageviews).

## Requirements

- Python 3.x
- Pandas
- SciPy

## Installation

To install the required Python libraries, use:

```bash
pip install pandas scipy
```
### Step 1: Clone the repository:

```bash
git clone https://github.com/venkatavinayvijjapu/Assignment.git
cd Hygwell Assignment-2
```

### Step 2: Run the notebook:
Run each cell in the notebook to see the analysis.(shift_enter)