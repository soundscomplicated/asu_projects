Analysis code for determining gender/sex themes in marketing and extrapolating gender/sex for unspecified gender/sex items

The file 'grouped_results.csv' can be used as stand in since I am not uploading the main data set due to personal identifying info. To use, simply delete the lines of code in these sections:
```
  # Load the data, drop anything that doesn't have a URL
  # fix URL screw up and shorten what can be shortened
  # regroup product families
```

Then, you should see a line that looks like this:
```
  # grouped_results = pd.read_csv('path/to/where/you/saved/the/file/named/grouped_results.csv')
```

You need to do 2 things:
  1. Delete the # and empty space before the word 'grouped'
  2. Change everything inside the parentheses and single quotes to the filepath where you saved the grouped_results.csv file. You need to make sure to leave the single quotes or nothing will work.

Now you are at a line that looks like this: 
```
  # result = grouped_results.copy()
```
Just delete the # and space before 'result'
