# Week 03 Recap

## Meeting goal
Select the v1 dataset and begin the first tickets.

## Dataset decision
We selected the NHANES derived stroke dataset for v1.

Why it was a strong v1 choice:
- Individual level dataset (person level)
- Has a stroke outcome label
- Rich set of features for risk scoring and prevention explanations
- Fastest path to shipping a credible v1 demo

We also reviewed other dataset options and what they are better suited for (future v2 work or storytelling use cases).  [Evaluation Sheet](https://docs.google.com/spreadsheets/d/1bNWgkLPjdjXMgkKiqFA409_IJX9uiyFBDFZ-t7Lyuwo/edit?gid=0#gid=0)

## What we did after selecting NHANES
- Started our first tickets
- Began the data dictionary work

## Key challenge we hit
- We ran into friction trying to find the “official” data dictionary on the NHANES website for the exact derived dataset fields
- This clarified that we may need to build our own plain English dictionary from the dataset column meanings and the source documentation we can find

## What’s next (Week 04)
- Split into lanes and execute tickets with real work time
- Finish the data dictionary and identify leakage columns
- Run a baseline model so we have an end to end pipeline