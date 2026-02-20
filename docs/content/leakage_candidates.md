# Leakage Candidates

This document flags **potential data leakage** and **reverse-causality risks** for the Stroke Prevention Demo dataset (NHANES-derived).

## What we mean by leakage here

The label `stroke` is **stroke history** (whether the participant reports ever being told they had a stroke). Because NHANES is cross-sectional, many features are measured **after** a stroke could have already happened. For a **prevention-style risk demo** (predicting future risk), some columns can act like "giveaways" because they may reflect **post-stroke consequences** or **post-stroke medical follow-up**.

- **Yes leakage**: should be excluded for a prevention-style model because it is the label itself or very likely a post-stroke proxy.
- **Maybe leakage**: time-order is unclear; could be a genuine risk factor *or* influenced by having had a stroke.

Because our modeling goal is to estimate future stroke risk, any variable that could reflect consequences of a past stroke (rather than pre-stroke risk factors) should be treated as potential leakage. Even if a variable is not the label itself, it may artificially inflate performance if it captures post-stroke health changes.

## Candidates

| Column name | Why it might leak | Leak? |
|---|---|---|
| stroke | This is the outcome label itself; if it appears in features it gives the answer away. | yes leakage |
| General health condition | Self-rated health can worsen after a stroke, making it a proxy for prior stroke-related disability/health status. | yes leakage |
| Minutes sedentary activity | Sedentary time can increase due to post-stroke mobility limitations, so it may encode the outcome indirectly. | yes leakage |
| depression | Depression can increase after a stroke, so it may reflect consequences rather than pre-stroke risk. | yes leakage |
| sleep disorder | A sleep disorder diagnosis can occur or be recorded after a stroke due to increased medical contact. | maybe leakage |
| sleep time | Sleep duration can change after major health events including stroke, so time-order is ambiguous. | maybe leakage |
| Coronary Heart Disease | Cardiovascular diagnoses can be discovered or recorded after a stroke during follow-up care, so direction is unclear. | maybe leakage |
| hypertension | High blood pressure is a real risk factor but may also be newly diagnosed after stroke-related clinical visits. | maybe leakage |
| diabetes | Diabetes is a risk factor but can be detected after stroke because of additional medical workups. | maybe leakage |
| high cholesterol | High cholesterol is a risk factor but may be diagnosed and treated after stroke, making timing ambiguous. | maybe leakage |
| smoke | Smoking behavior may change after a stroke (people quit), so current smoking status may reflect post-stroke behavior. | maybe leakage |
| alcohol  | Alcohol use may change after a stroke (reduction/cessation), so current use can reflect post-stroke behavior. | maybe leakage |

## Notes and how to use this list

- For the modeling tickets, create a single list like `LEAKAGE_DROP_COLS = [...]` and drop those columns from `X` **before** the train-test split.
- Start with the **yes leakage** items first; they are the most likely to inflate results in a prevention framing.

## Suggested first drop list

For the most conservative prevention-style baseline, drop these first:

- `General health condition`
- `Minutes sedentary activity`
- `depression`

Then optionally evaluate adding/removing the **maybe** items one at a time and compare the test ROC AUC.
