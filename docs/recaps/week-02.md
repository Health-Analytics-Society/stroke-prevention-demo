# Week 02 Recap


## Meeting goal
Review dataset options, do quick EDA, and decide what dataset is best for v1.

## What we did
- Explored multiple dataset options as a group
- Did early EDA (basic checks like column types, outcome label presence, missingness patterns, and how usable the dataset feels)
- Continued the “good data” discussion specifically for healthcare projects

## Mini lesson
### Data reliability and validity for healthcare
We focused on choosing data that is:
- Reliable: consistent, not messy, not full of unknown codes
- Valid: the outcome and features actually represent what we think they represent
- Documented: we can explain where it came from and what the columns mean
- Safe: avoids leakage and avoids decisions that distort populations

We also talked about why missingness can be dangerous:
- Dropping lots of rows can erase certain demographics and bias the dataset
- Heavy imputation can create fake patterns if huge chunks of data are missing

## What went well
- Strong discussion and reasoning around dataset quality
- The team started thinking like a real health data team instead of “just train a model”

## What was challenging
- Some silence gaps and uneven participation
- Technical setup troubleshooting during the meeting slowed momentum

## What’s next (Week 03)
- Make a final dataset selection for v1
- Start our first real project tickets (docs + pipeline work)