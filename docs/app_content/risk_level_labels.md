# Risk Level Labels

This file defines the plain-language risk categories shown in the Stroke Prevention Demo app.

Risk levels are based on where a user's predicted probability falls relative to the test-set score distribution from the baseline logistic regression model. These are for educational and illustrative purposes only — they are not clinical thresholds.

---

## Score cutoffs (from baseline model, test set)

Reported in `reports/baseline_metrics.md`:

| Statistic | Score |
|---|---|
| Minimum | 0.015 |
| 50th percentile (median) | 0.419 |
| 80th percentile | 0.622 |
| 95th percentile | 0.743 |
| Maximum | 0.905 |

---

## Risk level definitions

| Level | Score range | Plain-language label | Color (suggested) |
|---|---|---|---|
| Low | < 0.42 | Lower relative risk | Green |
| Moderate | 0.42 – 0.62 | Moderate relative risk | Yellow / Amber |
| High | > 0.62 | Higher relative risk | Red |

### Rationale for the cutoffs

- **Low (below median):** The score is below the 50th percentile of the test set. The model sees fewer co-occurring risk factors compared to the typical person in the dataset.
- **Moderate (median to 80th percentile):** The score is above average but not in the top 20%. Multiple modifiable risk factors may be present.
- **High (above 80th percentile):** The score is in the top 20% of the test set. Several high-weight risk factors are present. This level is intended to prompt the user to review the recommended next steps and speak with a healthcare provider.

---

## What these labels are NOT

- They are not clinical cut-offs. No medical organization has validated these thresholds.
- They do not represent an absolute probability of having a stroke. The underlying model is a logistic regression baseline and has not been externally validated.
- A "Low" score does not mean zero risk.
- A "High" score does not mean a stroke is certain or imminent.

See `docs/app_content/disclaimer_and_limitations.md` for full disclaimer language.

---

## Display copy (for the app)

Use these short strings in the Streamlit UI:

| Level | Headline | Supporting text |
|---|---|---|
| Low | Your score suggests lower relative risk. | Your inputs put you below the median in our model's test set. Keep up the healthy habits and stay current with regular checkups. |
| Moderate | Your score suggests moderate relative risk. | Several risk factors are present. Small, consistent lifestyle changes can meaningfully shift your risk profile over time. |
| High | Your score suggests higher relative risk. | Multiple high-weight risk factors are active in your profile. We encourage you to review the recommended next steps below and speak with a healthcare provider at your next opportunity. |

---

## Notes for the Docs + Content lane

- These cutoffs were derived from the test-set score distribution at the time the final demo baseline was run (see `reports/baseline_metrics.md`).
- If the model is retrained or the threshold is changed in the Config section of the training notebook, the cutoffs may shift. Re-run the notebook and update the cutoff table above to match.
- The three-level scheme (Low / Moderate / High) was chosen for simplicity. A four-level scheme (adding "Very High" above the 95th percentile ≈ 0.77) is straightforward to add if the team decides it is more informative.
